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