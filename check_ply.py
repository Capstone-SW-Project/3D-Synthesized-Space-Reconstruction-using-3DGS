import argparse
from plyfile import PlyData

# PLY 파일을 읽어서 내용을 출력하는 함수
def inspect_ply(filepath):
    try:
        # Load the PLY file
        plydata = PlyData.read(filepath)

        print("PLY Header:")
        for element in plydata.elements:
            print(f"Element: {element.name} ({element.count} instances)")
            for prop in element.properties:
                property_type = prop.name
                print(f"  Property: {prop.name} ({property_type})")

        print("\nPoint Cloud Data Preview:")

        if 'vertex' in plydata:
            vertex_data = plydata['vertex'].data[:10]
            for i, vertex in enumerate(vertex_data):
                print(f"Point {i + 1}: {tuple(vertex)}")
        else:
            print("No vertex data found.")
    except Exception as e:
        print(f"Error reading PLY file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check PLY file")
    parser.add_argument('-p', '--ply', type=str, required=True, help='path to ply file')
    args = parser.parse_args()

    inspect_ply(args.ply)

if __name__ == "__main__":
    main()