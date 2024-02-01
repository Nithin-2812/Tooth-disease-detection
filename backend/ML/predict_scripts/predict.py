from ultralytics import YOLO

def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou



def generate_results(image, disease_result, enum_result):
    disease_names = disease_result.names
    disease_boxes = disease_result.boxes

    enum_names = enum_result.names
    enum_boxes = enum_result.boxes

    results = {
        'disease_classes' : disease_names,
        'tooth_classes'   : enum_names,
        'detections'      : []
    }

    # Dictionary to store detected diseases for each tooth enumeration
    tooth_disease_mapping = {}

    # For each diseased tooth, compute IOU against enumeration so we can classify it to a specific tooth number
    for box in disease_boxes:
        highest = 0
        highestIOU = None
        for box2 in enum_boxes:
            val = bb_intersection_over_union(box.xyxy[0].tolist(), box2.xyxy[0].tolist())
            if val > highest:
                highest = val
                highestIOU = box2

        if highestIOU is not None:  # Check if tooth number was detected
            c, conf = int(highestIOU.cls), float(highestIOU.conf)
            disease_name = disease_names[int(box.cls)]
            tooth_num = str(enum_names[c])
            iou = highest

            # Append disease detection to the list of diseases for this tooth enumeration
            if tooth_num not in tooth_disease_mapping:
                tooth_disease_mapping[tooth_num] = []

            bbox_list = box.xywh.tolist()[0]
            tooth_disease_mapping[tooth_num].append({
                'disease': disease_name,
                'confidence': conf,
                'iou': iou,
                'coordinates': {
                'x'         : bbox_list[0],
                'y'         : bbox_list[1],
                'width'     : bbox_list[2],
                'height'    : bbox_list[3]
                }
            })
            print("Matched " + disease_name + " to " + enum_names[c] + " with IOU " + str(iou))
        else:
            disease_name = disease_names[int(box.cls)]
            disease_confidence = float(box.conf)
            print(f"No tooth number detected for diseased tooth with disease: {disease_name}")
            # Store information about undetected tooth number
            bbox_list = box.xywh.tolist()[0]
            results['detections'].append({
                'disease': disease_name,
                'tooth': 'Not detected',
                'confidence': disease_confidence,  # Store confidence of disease detection
                'coordinates': {
                'x'         : bbox_list[0],
                'y'         : bbox_list[1],
                'width'     : bbox_list[2],
                'height'    : bbox_list[3]
                }
            })

    # Populate the final results with all tooth enumeration detections and their associated diseases
    for tooth_num, diseases in tooth_disease_mapping.items():
        for disease_info in diseases:
            results['detections'].append({
                'disease': disease_info['disease'],
                'tooth': tooth_num,
                'confidence': disease_info['confidence'],
                'iou': disease_info['iou'],
                'coordinates': disease_info['coordinates']
            })


    #print(results['detections'])

    return results



def runPrediction(input):
    model_disease = YOLO('ML/models/Batch3_best.pt')
    results_disease = model_disease(input, imgsz=1280, conf=0.5)[0]

    model_enum = YOLO('ML/models/Enumeration_Model.pt')
    results_enum = model_enum(input, imgsz=1280, conf=0.5)[0]

    return generate_results(input, results_disease, results_enum)