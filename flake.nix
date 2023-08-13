{
  description = "Mapping Wikipedia pages together.";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pyenv = pkgs.python311.withPackages (p: with p; [
          aiosqlite
          requests
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            black
          ] ++ [ pyenv ];
        };

        packages = rec {
          wikipath = let 
            pypkgs = pkgs.python311Packages;
          in pypkgs.buildPythonPackage {
            pname = "wikipath";
            version = "0.0.1";
            src = ./.;

            propagatedBuildInputs = with pypkgs; [ aiosqlite requests ];
          };

          default = wikipath;
        };
      });
}