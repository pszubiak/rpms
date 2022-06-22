#! /bin/bash

set -euxo pipefail

version=2.0.23
prerel=

src=waf-${version}${prerel}.tar.bz2
dst=${src%.tar.bz2}.stripped.tar.bz2

readarray -t files <<-EOF
	waf-${version}/docs/sphinx/_images/waf-64x64.png
	waf-${version}/docs/slides/presentation/gfx/waflogo.svg
EOF

# tar's "--delete option has been reported to work properly when tar
# acts as a filter from stdin to stdout."
bzip2 -cd "${src}" | tar --delete "${files[@]}" | bzip2 -c > "${dst}"
touch -m -r "${src}" "${dst}"
