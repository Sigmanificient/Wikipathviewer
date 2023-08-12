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
      });
}
