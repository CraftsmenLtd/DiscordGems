resource "aws_dynamodb_table" "gems_table" {
  name           = "${var.prefix}-gem-count"
  read_capacity  = "5"
  write_capacity = "5"
  hash_key       = "uuid"

  attribute {
    name = "uuid"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  global_secondary_index {
    name               = "date-index"
    hash_key           = "date"
    write_capacity     = 5
    read_capacity      = 5
    projection_type    = "ALL"
    non_key_attributes = []
  }
}