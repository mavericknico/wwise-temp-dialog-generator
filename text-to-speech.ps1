 param (
    [Parameter(Mandatory=$true)][string]$path,
    [Parameter(Mandatory=$true)][string]$text,
    [Parameter(Mandatory=$true)][string]$voice
 )

Add-Type -AssemblyName System.Speech; 
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$synth.SetOutputToWaveFile($path);
$synth.SelectVoice($voice)
$synth.Speak($text);
$synth.Dispose();