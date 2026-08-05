# validate_v2.ps1 - Validador del esquema v2 (sentencias)
# Uso:  .\validate_v2.ps1              -> valida Outputs\*.v2.json
#       .\validate_v2.ps1 -Path ruta   -> valida otra carpeta o un archivo suelto
# Exit code: 0 si todo pasa, 1 si hay algun FAIL o si no hay nada que validar.
#
# Las rutas relativas se resuelven respecto a la ubicacion del script, no al
# directorio de trabajo. Se admite una ruta absoluta para validar otro conjunto.
#
# Nota: sin caracteres no-ASCII a proposito, para que la salida no dependa
# de la codepage de la consola.

param(
    [string]$Path = "Outputs",
    [string]$InputsDir = "Inputs",
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

# Las rutas relativas se resuelven respecto al script, no al directorio de
# trabajo. Asi el validador se comporta igual se lance desde donde se lance.
# Las rutas absolutas se respetan tal cual.
if (-not [System.IO.Path]::IsPathRooted($Path)) {
    $Path = Join-Path $PSScriptRoot $Path
}
if (-not [System.IO.Path]::IsPathRooted($InputsDir)) {
    $InputsDir = Join-Path $PSScriptRoot $InputsDir
}

# Inputs\ no se publica en el repositorio (ver README). Si no esta presente no
# se puede contrastar document_type contra la cabecera: en ese caso se valida
# solo la pertenencia al enum y se avisa una vez al final, en vez de marcar
# cada archivo.
$INPUTS_AVAILABLE = Test-Path $InputsDir -PathType Container

$SCHEMA_ORDER = @(
    'document_type', 'case_id', 'decision_date', 'court_or_body', 'ponente',
    'parties', 'facts', 'procedural_posture', 'legal_issues', 'applied_rules',
    'cited_by_parties', 'holding', 'ratio_summary', 'uncertainties',
    'document_quality_notes', 'next_review_questions'
)
$CASE_ID_KEYS = @('ecli', 'roj', 'resolution_number', 'appeal_number', 'id_cendoj')
$RULE_TYPES   = @('norma', 'jurisprudencia', 'doctrina')
$DOC_TYPES    = @('sentencia', 'auto')

# Marcadores de contenido procesal que no deberian aparecer en 'facts'.
$PROC_MARKERS = @(
    'recurso de casacion', 'infraccion procesal', 'interpuso recurso',
    'recurrio en apelacion', 'juzgado de primera instancia', 'juzgado de lo mercantil',
    'audiencia provincial', 'auto de admision', 'admitio los recursos',
    'desestimo el recurso', 'estimo el recurso', 'senalo para votacion',
    'dicto sentencia'
)

function Remove-Accents([string]$s) {
    if ($null -eq $s) { return "" }
    $n = $s.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object Text.StringBuilder
    foreach ($c in $n.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($c) -ne 'NonSpacingMark') {
            [void]$sb.Append($c)
        }
    }
    return $sb.ToString().ToLowerInvariant()
}

# Devuelve el 'Tipo de Resolucion:' de la cabecera del input correspondiente a un
# output, normalizado a minuscula y sin acentos. Devuelve $null si no se encuentra
# el input, y "" si el input existe pero no declara el campo.
# El input se busca en cualquier subcarpeta de Inputs\ (dev, test, ...), porque el
# output no registra de que conjunto procede.
function Get-HeaderDocType([string]$BaseName) {
    if (-not $INPUTS_AVAILABLE) { return $null }

    $candidates = @(Get-ChildItem -Path $InputsDir -Filter "$BaseName.txt" -Recurse -File -ErrorAction SilentlyContinue)
    if ($candidates.Count -eq 0) { return $null }

    # Solo la cabecera: el cuerpo puede contener la palabra en otros contextos.
    $head = Get-Content $candidates[0].FullName -TotalCount 15 -Encoding UTF8
    foreach ($line in $head) {
        $plain = Remove-Accents $line
        if ($plain -match '^\s*tipo de resolucion\s*:\s*(.+?)\s*$') {
            return (Remove-Accents $Matches[1]).Trim()
        }
    }
    return ""
}

# --- recoleccion de archivos ---
if (Test-Path $Path -PathType Leaf) {
    $files = @(Get-Item $Path)
} else {
    $files = @(Get-ChildItem (Join-Path $Path "*.v2.json") | Sort-Object Name)
}

if ($files.Count -eq 0) {
    Write-Output "No se encontraron archivos *.v2.json en '$Path'."
    exit 1
}

$totalFail = 0
$totalWarn = 0
$rows = @()

foreach ($f in $files) {
    $fails = New-Object System.Collections.ArrayList
    $warns = New-Object System.Collections.ArrayList

    # --- 0. JSON parseable ---
    $raw = $null; $o = $null
    try {
        $raw = Get-Content $f.FullName -Raw -Encoding UTF8
        $o = $raw | ConvertFrom-Json
    } catch {
        Write-Output "=== $($f.Name)"
        Write-Output "    FAIL  JSON no parseable: $($_.Exception.Message)"
        $totalFail++
        $rows += [pscustomobject]@{ Archivo = $f.Name; Estado = "FAIL"; Fails = 1; Warns = 0 }
        continue
    }

    if ($raw -match "�") { [void]$warns.Add("el archivo contiene caracteres de reemplazo (problema de codificacion)") }

    # --- 1. campos y orden ---
    $props = @($o.PSObject.Properties.Name)
    foreach ($k in $SCHEMA_ORDER) {
        if ($props -notcontains $k) { [void]$fails.Add("falta el campo '$k'") }
    }
    foreach ($k in $props) {
        if ($SCHEMA_ORDER -notcontains $k) { [void]$fails.Add("campo no previsto en el esquema: '$k'") }
    }
    if (($props -join ',') -ne ($SCHEMA_ORDER -join ',') -and $fails.Count -eq 0) {
        [void]$fails.Add("los campos no siguen el orden del esquema")
    }

    # --- 2. document_type: enum cerrado Y coincidencia con la cabecera ---
    # El nombre del archivo no es fuente: sentenciaN.txt puede contener un auto.
    $dt = $o.document_type
    if ($DOC_TYPES -notcontains $dt) {
        # Fuera del enum: contrastarlo ademas con la cabecera solo repetiria el
        # mismo defecto con otras palabras.
        [void]$fails.Add("document_type = '$dt' (debe ser 'sentencia' o 'auto')")
    } else {
        $base       = $f.Name -replace '\.v2\.json$', ''
        $headerType = Get-HeaderDocType $base

        if ($null -eq $headerType) {
            if ($INPUTS_AVAILABLE) {
                [void]$warns.Add("no se encontro el input '$base.txt': document_type sin contrastar")
            }
        } elseif ($headerType -eq "") {
            [void]$warns.Add("la cabecera de '$base.txt' no declara 'Tipo de Resolucion:'")
        } elseif ($headerType -ne $dt) {
            [void]$fails.Add("document_type = '$dt' pero la cabecera dice '$headerType'")
        }
    }

    # --- 3. case_id: al menos un identificador ---
    $ids = 0
    foreach ($k in $CASE_ID_KEYS) {
        if ($null -ne $o.case_id -and -not [string]::IsNullOrWhiteSpace([string]$o.case_id.$k)) { $ids++ }
    }
    if ($ids -eq 0) { [void]$fails.Add("case_id no contiene ningun identificador") }
    elseif ($ids -lt $CASE_ID_KEYS.Count) { [void]$warns.Add("case_id tiene $ids/5 identificadores") }

    # --- 4. decision_date ISO 8601 ---
    if ([string]$o.decision_date -notmatch '^\d{4}-\d{2}-\d{2}$') {
        [void]$fails.Add("decision_date '$($o.decision_date)' no tiene formato YYYY-MM-DD")
    }

    # --- 5. facts: ARRAY de 5-15 elementos ---
    if ($o.facts -is [string]) {
        [void]$fails.Add("facts es string; el esquema v2 exige un ARRAY")
    } else {
        $factsArr = @($o.facts)
        if ($factsArr.Count -lt 5 -or $factsArr.Count -gt 15) {
            [void]$fails.Add("facts tiene $($factsArr.Count) elementos (rango exigido: 5-15)")
        }
    }

    # --- 6. facts != procedural_posture ---
    $factsArr = @($o.facts)
    $factsJoined = ($factsArr -join ' ')
    $pp = [string]$o.procedural_posture
    if ([string]::IsNullOrWhiteSpace($pp)) {
        [void]$fails.Add("procedural_posture vacio")
    }
    if ($factsJoined.Trim() -eq $pp.Trim() -and $pp.Trim().Length -gt 0) {
        [void]$fails.Add("facts y procedural_posture son identicos")
    }
    # solapamiento: algun elemento de facts reproducido literalmente en procedural_posture
    $ppNorm = Remove-Accents $pp
    foreach ($fact in $factsArr) {
        $fNorm = Remove-Accents ([string]$fact)
        if ($fNorm.Length -gt 40 -and $ppNorm.Contains($fNorm)) {
            [void]$fails.Add("un elemento de facts aparece literalmente en procedural_posture")
            break
        }
    }
    # aviso: contenido procesal dentro de facts
    $hits = @()
    foreach ($fact in $factsArr) {
        $fNorm = Remove-Accents ([string]$fact)
        foreach ($m in $PROC_MARKERS) {
            if ($fNorm.Contains($m)) { $hits += $m }
        }
    }
    $hits = @($hits | Select-Object -Unique)
    if ($hits.Count -gt 0) {
        [void]$warns.Add("facts contiene marcadores procesales (revisar reparto con procedural_posture): " + ($hits -join ', '))
    }

    # --- 7. parties: array de objetos {name, role} ---
    $parties = @($o.parties)
    if ($parties.Count -eq 0) {
        [void]$fails.Add("parties vacio")
    } else {
        $bad = 0
        foreach ($p in $parties) {
            if ($p -is [string]) { $bad++; continue }
            $pk = @($p.PSObject.Properties.Name)
            if ($pk -notcontains 'name' -or $pk -notcontains 'role') { $bad++; continue }
            if ([string]::IsNullOrWhiteSpace([string]$p.name) -or [string]::IsNullOrWhiteSpace([string]$p.role)) { $bad++ }
        }
        if ($bad -gt 0) { [void]$fails.Add("$bad de $($parties.Count) elementos de parties no cumplen {name, role}") }
    }

    # --- 8. applied_rules: array de objetos {type, ref, note} ---
    $rules = @($o.applied_rules)
    if ($rules.Count -eq 0) {
        [void]$fails.Add("applied_rules vacio")
    } else {
        $badShape = 0; $badType = 0
        foreach ($r in $rules) {
            if ($r -is [string]) { $badShape++; continue }
            $rk = @($r.PSObject.Properties.Name)
            if ($rk -notcontains 'type' -or $rk -notcontains 'ref' -or $rk -notcontains 'note') { $badShape++; continue }
            if ([string]::IsNullOrWhiteSpace([string]$r.ref)) { $badShape++; continue }
            if ($RULE_TYPES -notcontains [string]$r.type) { $badType++ }
        }
        if ($badShape -gt 0) { [void]$fails.Add("$badShape de $($rules.Count) elementos de applied_rules no cumplen {type, ref, note}") }
        if ($badType -gt 0)  { [void]$fails.Add("$badType elementos de applied_rules tienen un 'type' fuera de {norma, jurisprudencia, doctrina}") }
    }

    # --- 9. applied_rules INTERSECCION cited_by_parties = vacio ---
    $cited = @($o.cited_by_parties)
    $collisions = @()
    foreach ($r in $rules) {
        if ($r -is [string]) { continue }
        $ref = [string]$r.ref
        if ([string]::IsNullOrWhiteSpace($ref)) { continue }
        $refNorm = Remove-Accents $ref
        if ($refNorm.Length -lt 8) { continue }
        foreach ($c in $cited) {
            $cNorm = Remove-Accents ([string]$c)
            if ($cNorm.Contains($refNorm) -or $refNorm.Contains($cNorm)) { $collisions += $ref }
        }
    }
    $collisions = @($collisions | Select-Object -Unique)
    if ($collisions.Count -gt 0) {
        [void]$fails.Add("applied_rules y cited_by_parties se solapan en: " + ($collisions -join ' | '))
    }

    # --- 10. ratio_summary: 3-8 elementos, <=400 caracteres ---
    if ($o.ratio_summary -is [string]) {
        [void]$fails.Add("ratio_summary es string; el esquema v2 exige un ARRAY")
    } else {
        $rs = @($o.ratio_summary)
        if ($rs.Count -lt 3 -or $rs.Count -gt 8) {
            [void]$fails.Add("ratio_summary tiene $($rs.Count) elementos (rango exigido: 3-8)")
        }
        $long = @($rs | Where-Object { ([string]$_).Length -gt 400 })
        if ($long.Count -gt 0) {
            $maxLen = ($rs | ForEach-Object { ([string]$_).Length } | Measure-Object -Maximum).Maximum
            [void]$fails.Add("$($long.Count) elementos de ratio_summary superan 400 caracteres (max $maxLen)")
        }
    }

    # --- 11. next_review_questions: 3-8 ---
    $nrq = @($o.next_review_questions)
    if ($nrq.Count -lt 3 -or $nrq.Count -gt 8) {
        [void]$fails.Add("next_review_questions tiene $($nrq.Count) elementos (rango exigido: 3-8)")
    }

    # --- 12. campos string no vacios ---
    foreach ($k in @('court_or_body', 'holding')) {
        if ([string]::IsNullOrWhiteSpace([string]$o.$k)) { [void]$fails.Add("$k vacio") }
    }
    if ([string]::IsNullOrWhiteSpace([string]$o.ponente)) {
        [void]$warns.Add("ponente vacio o null (permitido solo si no consta en el documento)")
    }

    # --- informe por archivo ---
    $estado = "OK"
    if ($fails.Count -gt 0) { $estado = "FAIL" }
    elseif ($warns.Count -gt 0) { $estado = "WARN" }

    if (-not $Quiet -or $estado -ne "OK") {
        Write-Output "=== $($f.Name) : $estado"
        foreach ($m in $fails) { Write-Output "    FAIL  $m" }
        foreach ($m in $warns) { Write-Output "    WARN  $m" }
        if ($estado -eq "OK") {
            Write-Output ("    facts={0}  legal_issues={1}  applied_rules={2}  cited_by_parties={3}  ratio_summary={4}  uncertainties={5}  doc_quality={6}  next_review={7}" -f `
                @($o.facts).Count, @($o.legal_issues).Count, @($o.applied_rules).Count, @($o.cited_by_parties).Count, `
                @($o.ratio_summary).Count, @($o.uncertainties).Count, @($o.document_quality_notes).Count, @($o.next_review_questions).Count)
        }
    }

    if ($fails.Count -gt 0) { $totalFail++ }
    $totalWarn += $warns.Count
    $rows += [pscustomobject]@{ Archivo = $f.Name; Estado = $estado; Fails = $fails.Count; Warns = $warns.Count }
}

Write-Output ""
Write-Output "--- RESUMEN ---"
$rows | Format-Table -AutoSize | Out-String | Write-Output
Write-Output ("{0} archivos | {1} con FAIL | {2} avisos" -f $files.Count, $totalFail, $totalWarn)

if (-not $INPUTS_AVAILABLE) {
    Write-Output ""
    Write-Output "NOTA: no se encontro '$InputsDir'. document_type se ha validado solo contra"
    Write-Output "      el enum; no se ha podido contrastar con la cabecera del documento."
}

if ($totalFail -gt 0) { exit 1 } else { exit 0 }
