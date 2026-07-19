FROM httpd:2.4.49

# Deploy the (boring, innocuous) static site into the default docroot.
COPY site/ /usr/local/apache2/htdocs/

# Entrypoint script writes the flag file (from the FLAG env var) outside
# the docroot at container start time.
COPY docker-entrypoint.sh /usr/local/apache2/bin/docker-entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/apache2/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/apache2/bin/docker-entrypoint.sh

# NOTE: this is intentionally NOT "hardening" the server. The stock
# httpd:2.4.49 image ships its <Directory /> block set to
# "Require all denied", which was not the reality of the vast majority of
# real-world httpd 2.4.49 deployments at the time CVE-2021-41773 was mass
# exploited (most admins never touched the root <Directory> block, and many
# distro / third-party base images and manual installs left filesystem
# access open). We restore that common real-world default here -- flipping
# "Require all denied" to "Require all granted" on <Directory /> only --
# leaving every other line of the stock config file untouched.
RUN sed -i '/<Directory \/>/,/<\/Directory>/ s/Require all denied/Require all granted/' /usr/local/apache2/conf/httpd.conf

EXPOSE 80

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["httpd-foreground"]
