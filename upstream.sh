#!/bin/bash

sleep .5
PROXY_IP_PORT=$1
USER_PASS=$2
PROXY_PORT=$3

AUTH_BASE64=$(echo -n "$USER_PASS" | base64)


if haproxy -v >/dev/null 2>&1; then
    echo "✅ HAProxy đã được cài đặt thành công!"
else
    echo "❌ Lỗi khi cài đặt HAProxy. Kiểm tra lại kết nối mạng hoặc repo CentOS."
    exit 1
fi

echo "📂 Sao lưu cấu hình HAProxy cũ..."
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak

echo "🛠️ Đang thiết lập cấu hình mới cho HAProxy..."

cat <<EOF | sudo tee /etc/haproxy/haproxy.cfg
defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend no_auth_proxy
    bind *:$PROXY_PORT
    default_backend auth_proxy_backend

backend auth_proxy_backend
    http-request set-header Proxy-Authorization Basic\ $AUTH_BASE64
    server proxy_auth $PROXY_IP_PORT
EOF

echo "🚀 Khởi động lại HAProxy..."
sudo systemctl restart haproxy
sudo systemctl enable haproxy

echo "🔍 Kiểm tra trạng thái HAProxy..."
sudo systemctl status haproxy --no-pager

echo "✅ HAProxy đã được thiết lập thành công!"
echo "💡 Proxy No-Auth đang chạy trên: http://$(hostname -I | awk '{print $1}'):$PROXY_PORT"
