{ pkgs, pypkgs, ... }: pypkgs.buildPythonPackage rec {
  pname = "arcade";
  version = "3.0";
  pyproject = true;

  #src = pkgs.fetchFromGitHub {
  #  owner = "pythonarcade";
  #  repo = "arcade";
  #  rev = version;
  #  sha256 = "sha256-sEFrTPPl/eWd8z180tMnIF1wzz/wNpQ9h+Cy4RheClk=";
  #};
  src = pypkgs.fetchPypi {
    pname = "arcade";
    inherit version;
    sha256 = "sha256-xxP2T/r0ML9tB0D5alvNSS/LuDh0574w9FOmsWp+tfY=";
  };

  build-system = with pypkgs; [ setuptools ];

  dependencies = with pypkgs; [
    (pyglet.overrideAttrs rec {
      version = "2.1.2";
      src = fetchPypi {
        pname = "pyglet";
        inherit version;
        sha256 = "sha256-b8H+1V623IDIenpFrGLCphvgjNMRFLJ6vvhhmVm+eEU=";
      };
    })
    (pillow.overrideAttrs rec {
      version = "11.0.0";
      src = fetchPypi {
        pname = "pillow";
        inherit version;
        sha256 = "sha256-crrLrySsAD/qm/+YN9Hu22CIdY1B4QDBVSkwFR9ndzk=";
      };
    })
    (pymunk.overrideAttrs rec {
      version = "6.9.0";
      src = fetchPypi {
        pname = "pymunk";
        inherit version;
        sha256 = "sha256-dl98VhqFmhtWW8UXpHzDmS1iWOhg+RdMUzAzwhivY8M=";
      };
    })
    (import ./python-pytiled.nix { inherit pkgs pypkgs; })
  ];
}
