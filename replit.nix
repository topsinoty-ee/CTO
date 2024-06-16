{pkgs}: {
  deps = [
    pkgs.nodePackages.prettier
    pkgs.libxcrypt
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
  ];
}
