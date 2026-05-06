from detection.detector import SatelliteDetector
import os


def test_thresholds():
    detector = SatelliteDetector()
    image_path = 'lampung_test_sample.tif'

    if not os.path.exists(image_path):
        print("File " + image_path + " not found.")
        return

    for conf in [0.25, 0.1, 0.05]:
        print("\nTesting with confidence " + str(conf) + "...")
        results = detector.run_detection(image_path, conf=conf)
        count = len(results['features'])
        print("Detected: " + str(count) + " objects")
        if count > 0:
            for feat in results['features'][:3]:
                props = feat['properties']
                print("  - " + str(props['class']) + " (" + str(round(props['confidence'], 2)) + ")")


if __name__ == "__main__":
    test_thresholds()
