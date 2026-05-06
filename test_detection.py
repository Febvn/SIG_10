from detection.detector import SatelliteDetector
import geojson
import os


def test():
    detector = SatelliteDetector()
    image_path = 'lampung_test_sample.tif'

    if not os.path.exists(image_path):
        print("Error: " + image_path + " not found.")
        return

    print("Running detection on " + image_path + "...")
    results = detector.run_detection(image_path)

    output_path = 'test_result.geojson'
    with open(output_path, 'w') as f:
        geojson.dump(results, f)

    count = len(results['features'])
    print("Detection complete! Found " + str(count) + " objects.")
    print("Results saved to " + output_path)


if __name__ == "__main__":
    test()
