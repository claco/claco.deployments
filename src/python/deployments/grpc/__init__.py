import os, sys

# Fix protoc generated `import` statement issues
# See https://github.com/protocolbuffers/protobuf/issues/7061
current_python_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_python_path)
