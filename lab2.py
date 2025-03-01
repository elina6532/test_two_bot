# Характеристики трех компьютеров
computer1 = {
    "CPU Frequency": "3.5 GHz",
    "Cores": "4",
    "RAM": "8 GB",
    "GPU Memory": "4 GB",
    "Disk Space": "500 GB",
    "Windows Version": "Windows 10"
}

computer2 = {
    "CPU Frequency": "2.8 GHz",
    "Cores": "2",
    "RAM": "4 GB",
    "GPU Memory": "2 GB",
    "Disk Space": "256 GB",
    "Windows Version": "Windows 8"
}

computer3 = {
    "CPU Frequency": "4.0 GHz",
    "Cores": "8",
    "RAM": "16 GB",
    "GPU Memory": "6 GB",
    "Disk Space": "1 TB",
    "Windows Version": "Windows 11"
}

# Вывод информации о каждом компьютере
for i, computer in enumerate([computer1, computer2, computer3], start=1):
    print(f"Computer {i}:")
    for key, value in computer.items():
        print(f"  {key}: {value}")
    print()