# ============================================================
#  eval_gold.ps1
#  Compara Outputs/sentenciaN.v2.json contra Gold/sentenciaN.gold.json
#  y calcula precision por campo.
#
#  Uso:  .\eval_gold.ps1
#        .\eval_gold.ps1 -Verbose1  (muestra tambien los aciertos)
#
#  Exit code: 0 si se evaluaron todos los Gold disponibles,
#             1 si falta algun output, si algun JSON es invalido
#             o si no se pudo comparar ningun campo.
#
#  Todas las rutas (Gold, Outputs y progress\METRICS.md) se resuelven
#  respecto a la ubicacion del script, no al directorio de trabajo.
#  Se puede pasar una ruta absoluta a -GoldDir o -OutputsDir para
#  evaluar otro conjunto.
# ============================================================

param(
    [string]$GoldDir    = "Gold",
    [string]$OutputsDir = "Outputs",
    [switch]$Verbose1
)

# Las rutas relativas se resuelven respecto al script, no al directorio de
# trabajo. Asi el script se comporta igual se lance desde donde se lance.
# Las rutas absolutas se respetan tal cual.
if (-not [System.IO.Path]::IsPathRooted($GoldDir)) {
    $GoldDir = Join-Path $PSScriptRoot $GoldDir
}
if (-not [System.IO.Path]::IsPathRooted($OutputsDir)) {
    $OutputsDir = Join-Path $PSScriptRoot $OutputsDir
}

# Mapa: campo del Gold (plano)  ->  ruta en el Output (anidada)
$fields = @(
    @{ Name = "ecli";              Path = "case_id.ecli" },
    @{ Name = "roj";               Path = "case_id.roj" },
    @{ Name = "resolution_number"; Path = "case_id.resolution_number" },
    @{ Name = "appeal_number";     Path = "case_id.appeal_number" },
    @{ Name = "id_cendoj";         Path = "case_id.id_cendoj" },
    @{ Name = "decision_date";     Path = "decision_date" },
    @{ Name = "court_or_body";     Path = "court_or_body" },
    @{ Name = "ponente";           Path = "ponente" }
)

function Get-NestedValue {
    param($Object, [string]$Path)
    $current = $Object
    foreach ($part in $Path.Split('.')) {
        if ($null -eq $current) { return $null }
        if ($current.PSObject.Properties.Name -contains $part) {
            $current = $current.$part
        } else {
            return $null
        }
    }
    return $current
}

# "" y null se tratan como el mismo valor: ausencia de dato
function Normalize {
    param($Value)
    if ($null -eq $Value) { return $null }
    $s = ([string]$Value).Trim()
    if ($s -eq "") { return $null }
    return $s
}

function Show-Value {
    param($Value)
    if ($null -eq $Value) { return "<null>" }
    return $Value
}

# ------------------------------------------------------------
# Recorrer los Gold disponibles
# ------------------------------------------------------------

$goldFiles = Get-ChildItem -Path $GoldDir -Filter "*.gold.json" -ErrorAction SilentlyContinue |
             Sort-Object { [int]($_.BaseName -replace '\D','') }

if (-not $goldFiles) {
    Write-Host "No se han encontrado archivos en $GoldDir" -ForegroundColor Red
    exit 1
}

$results  = @()
$skipped  = @()

foreach ($gf in $goldFiles) {

    $num        = ($gf.BaseName -replace '\D','')
    $outputPath = Join-Path $OutputsDir "sentencia$num.v2.json"

    if (-not (Test-Path $outputPath)) {
        $skipped += "sentencia$num  (falta el output)"
        continue
    }

    try {
        $gold   = Get-Content $gf.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
        $output = Get-Content $outputPath  -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        $skipped += "sentencia$num  (JSON invalido: $($_.Exception.Message))"
        continue
    }

    foreach ($f in $fields) {

        $gVal = Normalize (Get-NestedValue $gold   $f.Name)
        $oVal = Normalize (Get-NestedValue $output $f.Path)

        if ($gVal -ceq $oVal) {
            $status = "OK"
        } elseif ($null -ne $gVal -and $null -ne $oVal -and $gVal -eq $oVal) {
            $status = "CASE"      # solo difiere en mayusculas/acentos de capitalizacion
        } elseif ($null -eq $gVal -and $null -ne $oVal) {
            $status = "INVENTADO" # el agente rellena algo que no esta en el documento
        } elseif ($null -ne $gVal -and $null -eq $oVal) {
            $status = "OMITIDO"   # el dato existe pero el agente no lo extrae
        } else {
            $status = "ERROR"
        }

        $results += [PSCustomObject]@{
            Doc    = "sentencia$num"
            Campo  = $f.Name
            Gold   = Show-Value $gVal
            Output = Show-Value $oVal
            Estado = $status
        }
    }
}

# ------------------------------------------------------------
# Resumen por campo
# ------------------------------------------------------------

Write-Host ""
Write-Host "=== PRECISION POR CAMPO ===" -ForegroundColor Cyan
Write-Host ""

$summary = foreach ($f in $fields) {
    $rows  = $results | Where-Object { $_.Campo -eq $f.Name }
    $total = $rows.Count
    $ok    = ($rows | Where-Object { $_.Estado -eq "OK" }).Count
    $pct   = if ($total -gt 0) { [math]::Round(100 * $ok / $total, 1) } else { 0 }

    [PSCustomObject]@{
        Campo    = $f.Name
        Aciertos = "$ok/$total"
        Precision = "$pct %"
    }
}

$summary | Format-Table -AutoSize

$totalAll = $results.Count
$okAll    = ($results | Where-Object { $_.Estado -eq "OK" }).Count
$pctAll   = if ($totalAll -gt 0) { [math]::Round(100 * $okAll / $totalAll, 1) } else { 0 }

Write-Host "GLOBAL: $okAll/$totalAll  ($pctAll %)" -ForegroundColor Yellow
Write-Host ""

# ------------------------------------------------------------
# Detalle de fallos
# ------------------------------------------------------------

$fails = $results | Where-Object { $_.Estado -ne "OK" }

if ($fails) {
    Write-Host "=== DISCREPANCIAS ===" -ForegroundColor Cyan
    Write-Host ""
    $fails | Format-Table Doc, Campo, Estado, Gold, Output -AutoSize
} else {
    Write-Host "Sin discrepancias." -ForegroundColor Green
}

if ($Verbose1) {
    Write-Host "=== ACIERTOS ===" -ForegroundColor DarkGray
    $results | Where-Object { $_.Estado -eq "OK" } | Format-Table Doc, Campo, Gold -AutoSize
}

if ($skipped) {
    Write-Host "=== OMITIDOS ===" -ForegroundColor DarkYellow
    $skipped | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
}

# ------------------------------------------------------------
# Guardar metricas
# ------------------------------------------------------------

# Ruta relativa al script, no al directorio de trabajo: si no, ejecutar el
# script desde otra carpeta escribe las metricas en el sitio equivocado.
$metricsDir = Join-Path $PSScriptRoot "progress"
if (-not (Test-Path $metricsDir)) { New-Item -ItemType Directory $metricsDir | Out-Null }
$metricsPath = Join-Path $metricsDir "METRICS.md"

$stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$block = @()
$block += ""
$block += "## $stamp"
$block += ""
$block += "Documentos evaluados: $($goldFiles.Count - $skipped.Count)"
$block += ""
$block += "| Campo | Aciertos | Precision |"
$block += "|---|---|---|"
foreach ($s in $summary) {
    $block += "| $($s.Campo) | $($s.Aciertos) | $($s.Precision) |"
}
$block += "| **GLOBAL** | **$okAll/$totalAll** | **$pctAll %** |"
$block += ""

if (-not (Test-Path $metricsPath)) {
    "# METRICAS - Extraccion de sentencias" | Out-File $metricsPath -Encoding UTF8
}
$block | Out-File $metricsPath -Encoding UTF8 -Append

Write-Host "Metricas guardadas en $metricsPath" -ForegroundColor DarkGray

# ------------------------------------------------------------
# Exit code
# ------------------------------------------------------------
# Una tirada con outputs ausentes o ilegibles no puede considerarse exitosa:
# de otro modo un fallo total pasaria en verde al encadenar el script.

if (@($skipped).Count -gt 0) {
    Write-Host ""
    Write-Host "FALLO: $(@($skipped).Count) documento(s) sin evaluar." -ForegroundColor Red
    exit 1
}

if ($totalAll -eq 0) {
    Write-Host ""
    Write-Host "FALLO: no se comparo ningun campo." -ForegroundColor Red
    exit 1
}

exit 0
