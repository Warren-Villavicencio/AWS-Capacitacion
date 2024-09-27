# Generar claves de acceso root
aws configure --profile root-mfa-delete-demo

# Activar mfa delete
aws s3api put-bucket-versioning --bucket blockstellart-demo-mfa-delete --versioning-configuration Status=Enabled,MFADelete=Enabled --mfa "arn-of-mfa-device mfa-code" --profile root-mfa-delete-demo

# Desactivar mfa delete
aws s3api put-bucket-versioning --bucket blockstellart-demo-mfa-delete --versioning-configuration Status=Enabled,MFADelete=Disabled --mfa "arn-of-mfa-device mfa-code" --profile root-mfa-delete-demo

# Elimina las credenciales de root en la consola IAM