__author__ = 'Sebastijan'

import cv2
import numpy

from DataManipulations import DataCollector, Plotter, collect_vectors
import ActiveShapeModel
import utils
from Preprocess import Preprocessor


def example_reading_landmarks_and_display_shape():
    TmpObj = DataCollector('../data/Landmarks/original/landmarks1-1.txt')
    Plotter.render_landmarks(TmpObj)


def example_read_landmarks_and_plot_over_original_image():
    TmpObj = DataCollector('../data/Landmarks/original/landmarks1-4.txt')
    img = cv2.imread('../data/Radiographs/01.tif')
    Plotter.render_over_image(TmpObj, img)


def example_collect_landmarks_from_multiple_teeth():
    res = collect_vectors('../data/Landmarks/original', '1', 80)
    print res


def example_calculate_mean_image_and_display():
    res = collect_vectors('../data/Landmarks/original', '5', 80)
    referent = ActiveShapeModel.ReferentModel(res)
    data_coll = DataCollector(None)
    res = referent.mean_model()
    data_coll.read_vector(referent.mean_model())

    Plotter.render_landmarks(data_coll)


def example_translate_to_origin():
    tmpObj = DataCollector('../data/Landmarks/original/landmarks1-1.txt')
    print numpy.mean(tmpObj.points, axis=0)
    tmpObj.translate_to_origin()
    print tmpObj.centroid


def example_scaling_to_unit_and_back():
    tmpObj = DataCollector('../data/Landmarks/original/landmarks1-1.txt')
    print tmpObj.points
    print "*" * 50
    tmpObj.scale_to_unit()
    print "centroid distance: ", tmpObj.check_distance()
    tmpObj.rescale()
    print tmpObj.points


def example_rotating_landmarks():
    tmpObj = DataCollector('../data/Landmarks/original/landmarks1-1.txt')
    Plotter.render_landmarks(tmpObj)

    tmpObj.rotate(1)
    Plotter.render_landmarks(tmpObj)


def example_aligning_model():
    res = collect_vectors('../data/Landmarks/original', '1', 80)

    #aligning the model
    referent = ActiveShapeModel.ReferentModel(res)
    referent.align()
    referent.rescale_and_realign()

    #retrieving the mean model
    model = referent.retrieve_mean_model()
    Plotter.render_landmarks(model)


def example_align_model_and_visualize_shapes():
    res = collect_vectors('../data/Landmarks/original', '4', 80)

    referent = ActiveShapeModel.ReferentModel(res)
    referent.align()
    referent.rescale_and_realign()

    for shape in referent.points:
        Plotter.render_landmarks(shape)


def example_calculate_principal_components():
    res = collect_vectors('../data/Landmarks/original', '7', 80)

    referent = ActiveShapeModel.ReferentModel(res)
    referent.align()
    referent.rescale_and_realign()

    variance = ActiveShapeModel.VarianceModel(referent)
    variance.obtain_components()

    print variance.get_components()
    print "Component variance ratio: ", variance.get_variances_explained()
    print "Eigenvalues: ", variance.get_eigenvalues()


def example_examine_principal_components():

    res = collect_vectors('../data/Landmarks/original', '1', 80)

    referent = ActiveShapeModel.ReferentModel(res)
    referent.align()
    referent.rescale_and_realign()

    variance = ActiveShapeModel.VarianceModel(referent)
    variance.obtain_components()

    components = variance.get_components()
    eigenvals = variance.get_eigenvalues()

    shapes = utils.vary_component(referent.mean_shape, components.transpose(), eigenvals, 0, 10)

    tmpObj = DataCollector(None)
    Plotter.render_landmarks(referent.mean_shape)

    for ind in range(len(shapes)):
        tmpObj.read_vector(shapes[ind, :])
        Plotter.render_landmarks(tmpObj)


def example_clean_image():
    img = cv2.imread('../data/Radiographs/01.tif')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_top = Preprocessor.top_hat_transform(img)
    img_bottom = Preprocessor.bottom_hat_transform(img)

    Plotter.display_image(img, 'Original image')
    Plotter.display_image(img_top, 'Top hat filtered')
    Plotter.display_image(img_bottom, 'Bottom hat filtered')
    img = cv2.add(img, img_top)
    img = cv2.subtract(img, img_bottom)

    Plotter.display_image(img, 'Result')