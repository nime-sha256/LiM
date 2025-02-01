import os
import pyshark
from tqdm import tqdm
import pandas as pd

# Parent path of the dataset which includes traffic session pcaps of classes as subfolders 
# Dataset should be in the following format:
# dataset_path/
# ├── class1/
# │   ├── session1.pcap
# │   ├── session2.pcap
# │   └── ...
# ├── class2/
# │   ├── session1.pcap
# │   ├── session2.pcap
# │   └── ...
# └── ...
dataset_path = 'path/to/the/parent/folder/of/the/dataset/'

# Number of packets per session to be considered
no_of_packets_per_session = 5


def create_dataframe(no_of_packets_per_session):
    """
    Create a DataFrame to store the extracted features from the pcap files.
    """
    columns = []
    for i in range(no_of_packets_per_session):
        packet_number = 'p' + str(i + 1)
        column_temp = [
            packet_number + '_ip_total_len', 
            packet_number + '_ip_ttl', 
            packet_number + '_inter_arrival_time'
        ]
        columns.extend(column_temp)
    columns.append('label')
    df = pd.DataFrame(columns=columns)
    return df


def get_packets_with_encrypted_application_data(pcap_file_path, no_of_packets_per_session):
    """
    Extract packets containing encrypted application data from a pcap file using Pyshark.
    """
    packets_with_encrypted_payload = []
    try:
        with pyshark.FileCapture(pcap_file_path, display_filter='tls') as capture:
            for packet in capture:
                try:
                    # Ensure the packet has a TLS layer and check for app_data without handshake info.
                    if hasattr(packet, 'tls'):
                        if hasattr(packet.tls, 'app_data') and not hasattr(packet.tls, 'handshake'):
                            packets_with_encrypted_payload.append(packet)
                    # Stop if the desired number of packets has been collected.
                    if len(packets_with_encrypted_payload) >= no_of_packets_per_session:
                        break
                except Exception as packet_error:
                    print(f"Error processing packet: {packet_error}")
                    continue
    except Exception as capture_error:
        print(f"Error opening capture file: {capture_error}")
    
    return packets_with_encrypted_payload


# Create the dataframe
df = create_dataframe(no_of_packets_per_session)

# Extract features from the pcap files
for parent, _, files in os.walk(dataset_path):
    if files:
        # Use os.path.basename for cross-platform compatibility
        label = os.path.basename(parent)
        print(f'Label - {label}')

        for file in tqdm(files):
            try:
                pcap_file_path = os.path.join(parent, file)
                session = []

                packets_with_application_data = get_packets_with_encrypted_application_data(
                    pcap_file_path, no_of_packets_per_session
                )

                if len(packets_with_application_data) == no_of_packets_per_session:
                    for i, packet in enumerate(packets_with_application_data):
                        ip_total_len = None
                        ip_ttl = None
                        
                        # Check if the IP layer exists in the Pyshark packet
                        if hasattr(packet, 'ip'):
                            # Casting to int as Pyshark usually returns string values.
                            ip_total_len = int(packet.ip.len) if hasattr(packet.ip, 'len') else None
                            ip_ttl = int(packet.ip.ttl) if hasattr(packet.ip, 'ttl') else None

                        # Calculate inter-arrival time using the packet's sniff timestamp
                        if i == 0:
                            inter_arrival_time = 0
                        else:
                            # Convert the sniff_timestamp to float for calculation.
                            inter_arrival_time = float(packet.sniff_timestamp) - float(packets_with_application_data[i - 1].sniff_timestamp)
            
                        packet_features = [ip_total_len, ip_ttl, inter_arrival_time]
                        session.extend(packet_features)

                    session.append(label)
                    df.loc[len(df)] = session
                else:
                    print(f"{pcap_file_path} : Less than {no_of_packets_per_session} encrypted packets found")
            
            except Exception as e:
                print(e)
                print(f"{pcap_file_path} : Error in extracting features")
                continue

# Ensure the dataset_path ends with the OS-specific separator.
dataset_path = os.path.join(dataset_path, '')

# Use os.path.basename to extract the last folder name for the output filename.
parent_folder_name = os.path.basename(os.path.normpath(dataset_path))
netmatrix_file_name = f"{parent_folder_name}_{no_of_packets_per_session}_packets.csv"
output_path = os.path.join('./', netmatrix_file_name)
df.to_csv(output_path, index=False)

print(f"Netmatrix file saved at {output_path}")
