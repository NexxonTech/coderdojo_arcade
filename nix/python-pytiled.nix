{ pkgs, pypkgs, ... }: pypkgs.buildPythonPackage rec {
  pname = "pytiled_parser";
  version = "2.2.9";
  pyproject = true;

  src = pkgs.fetchPypi {
    inherit pname version;
    sha256 = "sha256-IlJp/dN6/LzTt26j4sq2sedCOHAnEGBVmQ20P9dFHr0=";
  };

  build-system = with pypkgs; [ setuptools ];

  dependencies = with pypkgs; [
    attrs
    pip
    typing-extensions
  ];
}
