server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root /data;

    location @backend {
        proxy_pass http://service:8000;
    }

    location / {
        try_files $uri $uri/ @backend;
    }

    location ~* \.(?:jpg|jpeg|gif|png|ico|css|js)$ {
        root /data/static;
        log_not_found off;
        expires 90d;
    }

    error_page   404              /404.html;
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}