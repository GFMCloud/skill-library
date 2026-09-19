{
  # Per-project devshell template.
  #
  # Copy into a repo root, edit `packages`, then:
  #   direnv allow          # first time only
  #   cd .                  # shell is now active
  #
  # Deliberately covers both aarch64-darwin (the Air) and x86_64-linux /
  # aarch64-linux (homelab). Same flake, same pinned toolchain, both places —
  # that's the entire reason this layer is worth having.

  description = "project devshell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            # --- Python -----------------------------------------------------
            # Nix supplies the interpreter; uv supplies the libraries.
            #
            # Do NOT pull pandas/numpy/scipy from nixpkgs. Nix's Python
            # packaging is where most people give up — version skew against
            # PyPI, long rebuilds on a fanless laptop, and no good story for
            # a lockfile your CI also understands. uv handles deps in a
            # standard .venv from a standard uv.lock. Nix's job here is just
            # to guarantee everyone gets the same interpreter.
            python313
            uv
            ruff

            # --- Common tooling ---------------------------------------------
            jq
            just          # task runner; better than a README full of commands

            # --- Uncomment as needed ----------------------------------------
            # nodejs_22
            # go
            # opentofu
            # awscli2
            # postgresql_16
            # duckdb
          ];

          # Keep this quiet and fast. It runs on every `cd` into the project.
          shellHook = ''
            export PROJECT_ROOT="$PWD"

            # uv creates .venv in-tree; activate it if it exists.
            if [ -d .venv ]; then
              source .venv/bin/activate
            fi

            echo "devshell: $(python --version 2>&1) | uv $(uv --version 2>&1 | cut -d' ' -f2)"
          '';
        };
      });
}
