import json
import os
from pathlib import Path
from typing import Any
import requests
from dotenv import load_dotenv


class SdnClient:
    def __init__(self, config: dict[str, str]) -> None:
        self.base_url = config["base_url"].rstrip("/")
        self.timeout = int(config.get("timeout", "15"))
        self.session = requests.Session()
        self.session.verify = config.get("verify_tls", "true").lower() == "true"
        self.username = os.environ["SDN_USERNAME"]
        self.password = os.environ["SDN_PASSWORD"]
        self.token: str | None = None

    def generate_token(self) -> str:
        response = self.session.post(
            f"{self.base_url}/api/v1/ticket",
            json={"username": self.username, "password": self.password},
            headers={"Accept": "application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        token = self._find_token(response.json())
        if not token:
            raise ValueError("The ticket response did not contain a token.")
        self.token = token
        self.session.headers.update({"X-Auth-Token": token})
        return token

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        if not self.token:
            self.generate_token()
            response = self.session.request(
            method=method,
            url=f"{self.base_url}/{path.lstrip('/')}",
            headers={"Accept": "application/json"},
            json=payload,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json() if response.text.strip() else {}

    def get_devices(self) -> Any:
        return self.request("GET", "/api/v1/network-device")

    def get_services(self) -> Any:
        return self.request("GET", "/api/v1/wan/network-wide-setting")

    def get_network_health(self) -> Any:
        return self.request("GET", "/api/v1/network-health")

    def get_hosts(self, filters: dict[str, Any] | None = None) -> Any:
        return self.request("GET", "/api/v1/host", params=filters)

    def update_service(self, payload: dict[str, Any]) -> Any:
        return self.request(
            "PUT",
            "/api/v1/wan/network-wide-setting",
            payload,
        )

    def add_device(self, device: dict[str, Any]) -> Any:
        return self.request("POST", "/api/v1/network-device", device)

    @staticmethod
    def _find_token(data: Any) -> str | None:
        if not isinstance(data, dict):
            return None
        response = data.get("response")
        if isinstance(response, dict) and isinstance(response.get("serviceTicket"), str):
            return response["serviceTicket"]
        for key in ("Token", "token", "access_token", "authToken", "serviceTicket"):
            if isinstance(data.get(key), str):
                return data[key]
        return SdnClient._find_token(response)

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".env")
    with open(project_root / "config.json", encoding="utf-8") as file:
        config = json.load(file)

    client = SdnClient(config)
    print(
        "1. Get Network Device Status\n"
        "2. Get Services\n"
        "3. Get Network Health\n"
        "4. Get Hosts Status\n"
        "5. Update Service\n"
        "6. Add Network Device"
    )
    choice = input("Select an option: ").strip()

    if choice == "1":
        result = client.get_devices()
    elif choice == "2":
        result = client.get_services()
    elif choice == "3":
        result = client.get_network_health()
    elif choice == "4":
        filters_text = input(
            'Host filters as JSON (press Enter for none): '
        ).strip()
        filters = json.loads(filters_text) if filters_text else None
        result = client.get_hosts(filters)
    elif choice == "5":
        templates = config.get("service_templates", {})
        if not templates:
            print("No service templates found in config.json.")
            return

        service_names = list(templates)
        print("\nServices:")
        for index, service in enumerate(service_names, start=1):
            print(f"{index}. {service}")
        service_choice = int(input("Select a service: ").strip()) - 1
        service_name = service_names[service_choice]
        template = templates[service_name]
        fields = template[0] if isinstance(template, list) else template

        field_names = list(fields)
        print("\nFields:")
        for index, field in enumerate(field_names, start=1):
            print(f"{index}. {field} (current: {fields[field]})")
        field_choice = int(input("Select a field: ").strip()) - 1
        field_name = field_names[field_choice]
        fields[field_name] = input(f"New value for {field_name}: ").strip()
        result = client.update_service(
            {service_name: [fields] if isinstance(template, list) else fields}
        )
    elif choice == "6":
        result = client.add_device(json.loads(input("Device JSON: ")))
    else:
        print("Invalid option.")
        return
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
