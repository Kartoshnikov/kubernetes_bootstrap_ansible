http {
  upstream balancer {
     {% for item in ["first:80", "second:80"] -%}
     server {{ item }};
     {% endfor -%} 
  }

  server {
      listen 80;

      server_name testsite.com;

      rewrite ^ https://testsite.com$request_uri? permanent;
  }


  server {
      listen 443;

      server_name testsite.com;

      root /var/www/testsite.com;

      location / {
          try_files $uri /index.php?$args;
      }

      location ~ \.php$ {
          try_files $uri =404;
          fastcgi_split_path_info ^(.+\.php)(/.+)$;
          fastcgi_pass balancer;
          fastcgi_index index.php;
          include fastcgi_params;
      }
  }
}
