{pkgs}: {
  deps = [
    pkgs.python-launcher
    pkgs.nodePackages.prettier
    pkgs.libxcrypt
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
  ];
}
