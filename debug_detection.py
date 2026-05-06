from detection.detector import SatelliteDetector
import geojson
import os


def debug():
    detector = SatelliteDetector()
    image_path = 'lampung_test_sample.tif'

    if not os.path.exists(image_path):
        print("Error: " + image_path + " not found.")
        return

    print("--- Debugging " + image_path + " ---")

    thresholds = [0.1, 0.05, 0.01]
    for conf in thresholds:
        print("\nTesting with confidence: " + str(conf))
        results = detector.run_detection(image_path, conf=conf)
        count = len(results['features'])
        print("Found " + str(count) + " objects.")

        if count > 0:
            for i, feat in enumerate(results['features'][:5]):
                props = feat['properties']
                line = "  " + str(i + 1) + ". Class: " + str(props['class'])
                line += ", Conf: " + str(round(props['confidence'], 4))
                print(line)
            if count > 5:
                print("  ... and " + str(count - 5) + " more.")


if __name__ == "__main__":
    debug()
