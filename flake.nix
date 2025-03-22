{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs { inherit system; };
        pyenv = with pkgs; python3.withPackages (pypkgs: with pypkgs; [
          (import nix/python-arcade.nix { inherit pkgs pypkgs; })
        ]);
      in
        {
          packages.pyenv = pyenv;
          devShell = pkgs.mkShell {
            name = "coderdojo_arcade_dev";
            packages = with pkgs; [
              pyenv
              tiled
            ];
          };
        }
    );
}
