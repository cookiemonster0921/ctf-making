FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Build tools + runtime tools the player can use once they land in the shell
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    ca-certificates \
    git \
    gcc \
    make \
    libpam0g-dev \
    socat \
    openssh-client \
    vim-tiny \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Build a known-old, vulnerable sudo release (1.9.5p1) from source.
# This predates the 1.9.5p2 security fix, so we always get the vulnerable
# binary regardless of what the distro package mirrors carry at build time.
# ---------------------------------------------------------------------------
WORKDIR /usr/src
RUN wget -q https://www.sudo.ws/dist/sudo-1.9.5p1.tar.gz \
    && tar xzf sudo-1.9.5p1.tar.gz \
    && rm sudo-1.9.5p1.tar.gz

WORKDIR /usr/src/sudo-1.9.5p1
RUN ./configure --prefix=/usr --sysconfdir=/etc --with-secure-path \
        --disable-shadow --without-lecture --with-passprompt="[sudo] password for %p: " \
    && make -j"$(nproc)" \
    && make install

# make install places the binary at /usr/bin/sudo (matches distro layout,
# so it is guaranteed to be the first "sudo" found on PATH). Force correct
# setuid-root permissions.
RUN rm -f /usr/local/bin/sudo /usr/local/sbin/sudo || true
RUN chown root:root /usr/bin/sudo && chmod 4755 /usr/bin/sudo

# Sanity check baked into the image build: fail the build if we somehow
# ended up with a patched / different version.
RUN /usr/bin/sudo -V | head -n1 | grep -q "1.9.5p1"

# ---------------------------------------------------------------------------
# Unprivileged player account
# ---------------------------------------------------------------------------
RUN useradd -m -s /bin/bash player \
    && echo "player:player" | chpasswd

# player gets NO sudoers entry at all -- the point of this bug is that it
# doesn't matter.
RUN mkdir -p /etc/sudoers.d

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9001

ENTRYPOINT ["/entrypoint.sh"]
