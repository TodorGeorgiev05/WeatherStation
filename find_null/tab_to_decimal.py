input_path = 'C:/Users/Asus/Desktop/Science/data/old_data.csv'
output_path = 'C:/Users/Asus/Desktop/Science/data/clean_data.csv'

with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    fout.write('datetime,temp1,humidity,temp2,humidity2,pressure\n')
    
    for line in fin:
        line = line.strip().strip('"')
        parts = line.split('\t')
        fout.write(','.join(parts) + '\n')

print(f"CSV in: {output_path}")
