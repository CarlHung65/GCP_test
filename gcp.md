1. 啟用 IAP & API:
    1. 在 Google Cloud 控制台 導航至 Security (安全) > Identity-Aware Proxy。
    2. 確保已啟用 Cloud IAP API。
2. 設定 IAM 權限:
    1. 前往 IAM & Admin (IAM 與管理) > Permissions (權限) 頁面。
    2. 為需要存取 VM 的用戶 (個人或群組) 新增成員。
    3. 授予角色：選取 Cloud IAP > IAP-secured Tunnel User (用於 SSH/TCP 隧道) 或 IAP-secured Web App User (用於 Web 應用)。
3. 在整個專案中啟用 (推薦):
    1. 在 GCP Console 頂部的專案選單旁，切換到目標專案。
    2. 前往 Compute Engine > 中繼資料，為專案添加一個項目：
        - Key: enable-oslogin
        - Value: TRUE. 


## IAM & ADMIN
1. Compute OS Login (roles/compute.osLogin)：基本登入權限
2. Service Account User (roles/iam.serviceAccountUser)：非常重要。因為 VM 通常會掛載一個服務帳號，您必須有權限「使用」該帳號才能透過 OS Login 登入。
3. IAP-secured Tunnel User (roles/iap.tunnelInstances.accessViaIAP)：如果您是在沒有外部 IP 的環境下連線，則必須具備此權限。


## install docker on ubuntu
1. Set up Docker's apt repository.
```bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

2. Install the Docker packages.
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Verify that the installation is successful by running the hello-world image
```bash
sudo docker run hello-world
```

4. download MySQL images
```bash
sudo docker pull mysql:8.0.36
```

5. create container (一建立container就要給password)
```bash
sudo docker run -d \
  --name mysql8 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -p 3306:3306 \
  mysql:8.0.36
```

6. enter container
```bash
sudo docker exec -it <container_ID> /bin/bash
```

7. 建立和GCP主機內的MYSQL SERVER連線(我的3307指向MYSQL3306)
```bash
gcloud compute ssh tjr104 --zone asia-east1-c --project watchful-net-484213-s5 --tunnel-through-iap -- -L 3307:localhost:3306
```

8. IDE setting
127.0.0.1:3307