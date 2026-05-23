{{- define "ragsystem.fullname" -}}
{{- printf "%s-%s" .Chart.Name "backend" -}}
{{- end -}}

{{- define "ragsystem.frontendname" -}}
{{- printf "%s-%s" .Chart.Name "frontend" -}}
{{- end -}}
