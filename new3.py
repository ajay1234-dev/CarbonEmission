import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import os
import sys
import time

def decode_barcode(frame):
    if frame is None:
        raise ValueError("Frame is None")
    
    barcodes = decode(frame)
    if barcodes:
        # Assuming that we want to handle the first detected barcode
        barcode = barcodes[0]
        barcode_data = barcode.data.decode('utf-8')
        return barcode_data
    
    return None

def get_data_from_excel(decoded_value):
    excel_file = 'CarbonData.xlsx'
    sheet_name = 'Day2'
    output_file = 'G:/My Drive/spreadsheet/spreadsheet.xlsx'
    
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        if 'Barcode' not in df.columns:
            raise KeyError("Column 'Barcode' not found in the DataFrame.")
        
        decoded_value_str = str(decoded_value).strip()
        df['Barcode'] = df['Barcode'].astype(str).str.strip().str.replace('\xa0', '')
        
        result = df[df['Barcode'] == decoded_value_str]
        
        if result.empty:
            return f"No data found for barcode: {decoded_value}"
        
        if os.path.exists(output_file):
            existing_df = pd.read_excel(output_file)
            combined_df = pd.concat([existing_df, result], ignore_index=True)
        else:
            combined_df = result
        
        combined_df.to_excel(output_file, index=False)
        return f"Data for barcode {decoded_value} saved to {output_file}"
    
    except FileNotFoundError:
        return "Error: File not found."
    except KeyError as e:
        return str(e)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return str(e)

def process_barcode():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return False  # Indicate failure to open camera
    
    processed = False  # Flag to track if a barcode has been processed
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Failed to grab frame.")
                break
            
            decoded_value = decode_barcode(frame)
            
            if decoded_value and not processed:
                print("Decoded Barcode Value:", decoded_value)
                data = get_data_from_excel(decoded_value)
                print("Data from Excel:\n", data)
                processed = True  # Set flag to True to stop further processing
                break  # Exit the loop after processing the first barcode
            
            cv2.imshow('Video Frame', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    return True  # Indicate successful processing

def main():
    while True:
        if not process_barcode():
            print("Failed to process barcode. Restarting...")
        
        print("Restarting camera...")
        time.sleep(1)  # Optional: wait a bit before restarting the camera

if __name__ == "__main__":
    main()
