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
        starterpack = pkgs.stdenvNoCC.mkDerivation {
          pname = "coderdojo_arcade_starterpack";
          version = "0.1.0";

          src = ./.;

          installPhase = ''
            mkdir coderdojo_arcade_starterpack/
            cp -r assets/ platformer/ coderdojo_arcade_starterpack/

            mkdir $out
            ${pkgs.zip}/bin/zip -r $out/CoderDojoArcadeStarterpack.zip coderdojo_arcade_starterpack/
          '';
        };
      in
        {
          defaultPackage = starterpack;
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
