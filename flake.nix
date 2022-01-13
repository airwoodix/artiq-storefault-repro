{
  inputs.artiq.url = "github:m-labs/artiq";
  inputs.nixpkgs.follows = "artiq/nixpkgs";

  outputs = { self, nixpkgs, artiq }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
    rec {
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python3.withPackages (ps: with ps; [
            artiq.packages.x86_64-linux.artiq
            msgpack
            numpy
            rpyc
          ]))
        ];
      };
    };
}
