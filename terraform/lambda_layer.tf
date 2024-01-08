locals {
  lambda_python_version     = "python3.10"
  requirements_filepath     = "${path.module}/../requirements.txt"
  lambda_layer_zipfile_name = "craftsmen-bot-layer"

  # WARNING: Do not change it
  lambda_layer_dir = "${path.module}/python"
}

resource "null_resource" "build_lambda_layer" {
  provisioner "local-exec" {
    when    = create
    command = "pip install -r ${local.requirements_filepath} --target ${local.lambda_layer_dir} && zip -r ${local.lambda_layer_zipfile_name}.zip ./${local.lambda_layer_dir} && rm -R ${local.lambda_layer_dir}"
  }

  triggers = {
    run_when_dependency = filemd5(local.requirements_filepath)
    run_when_source     = sha1(join("", [for f in fileset(path.root, "${path.module}/../src/**") : filesha1(f)]))
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = "${local.lambda_layer_zipfile_name}.zip"
  layer_name          = "${var.prefix}-lambda-layer"
  compatible_runtimes = [local.lambda_python_version]
  depends_on          = [null_resource.build_lambda_layer]
  description         = filemd5(local.requirements_filepath)
}
