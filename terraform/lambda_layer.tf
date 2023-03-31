locals {
  lambda_python_version = "python3.8"
  lambda_artifact_dir   = "${path.module}/layer_zip"
  lambda_layer_filepath = data.external.build_lambda_layer.result.zipfile_path
}

data "external" "build_lambda_layer" {
  program = ["/bin/bash", "-c", "${path.module}/build_layer.sh"]

  query = {
    DESTINATION_DIR = abspath(local.lambda_artifact_dir)
    MODULE_DIR      = abspath(path.module)
    ZIPFILE_NAME    = "craftsmen-bot-layer"
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = local.lambda_layer_filepath
  source_code_hash    = filebase64sha256(local.lambda_layer_filepath)
  layer_name          = "craftsmen-bot-layer"
  compatible_runtimes = [local.lambda_python_version]

  lifecycle {
    create_before_destroy = true
  }
}
