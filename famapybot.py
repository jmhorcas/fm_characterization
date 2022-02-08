import os
import logging 
import requests
import multiprocessing

import telebot 

import numpy as np
import matplotlib.pyplot as plt

from famapy.metamodels.pysat_metamodel.transformations.fm_to_pysat import FmToPysat
from famapy.metamodels.cnf_metamodel.transformations.pysat_to_cnf import PysatToCNF
from famapy.metamodels.bdd_metamodel.transformations.cnf_to_bdd import CNFToBDD
from famapy.metamodels.fm_metamodel.transformations.featureide_parser import FeatureIDEParser
from famapy.metamodels.fm_metamodel.operations.metrics import Metrics
from famapy.metamodels.fm_metamodel.operations import get_core_features, average_branching_factor, max_depth_tree, count_configurations
from famapy.metamodels.bdd_metamodel.operations.fm_operations import BDDProductDistributionBF, BDDNumberOfConfigurations
from famapy.metamodels.pysat_metamodel.operations.glucose3_products import Glucose3Products


HTTP_API_TOKEN = '1865270990:AAHuKC7Kjqjr-wpIbJRDZOvi4vrsrUDOU8Y'


def int_to_scientific_notation(n: int, precision: int = 2) -> str:
    """Convert a large int into scientific notation.
    
    It is required for large numbers that Python cannot convert to float,
    solving the error `OverflowError: int too large to convert to float`.
    """
    str_n = str(n)
    decimal = str_n[1:precision+1]
    exponent = str(len(str_n) - 1)
    return str_n[0] + '.' + decimal + 'e' + exponent


def analyze_model(file_name: str) -> str:
    fm = FeatureIDEParser(file_name).transform() 
    metrics = Metrics(fm)
    response = f"*Root:* {fm.root.name}\n"
    response += f"*Features:* {metrics.nof_features()}\n"
    response += f"*Cross-tree constraints:* {metrics.nof_cross_tree_constraints()}\n"
    nof_configs = count_configurations(fm)
    response += f"*Configurations:* {'≤' if metrics.nof_cross_tree_constraints() > 0 else ''} {int_to_scientific_notation(nof_configs) if nof_configs > 1e6 else nof_configs}\n"
    response += f"*Group-features:* {metrics.nof_group_features()}\n"
    response += f"*Alternative-groups:* {metrics.nof_alternative_groups()}\n"
    response += f"*Or-groups:* {metrics.nof_or_groups()}\n"
    response += f"*Abstract features:* {metrics.nof_abstract_features()}\n"
    response += f"*Leaf features:* {metrics.nof_leaf_features()}\n"
    response += f"*Core features:* {len(get_core_features(fm))}\n"
    response += f"*Max depth tree:* {max_depth_tree(fm)}\n"
    response += f"*Branching factor:* {average_branching_factor(fm)}\n"

    print(fm)
    print(fm.root.get_relations())
    for r in fm.root.get_relations():
        print([f for f in r.children])
    return response


def get_product_distribution(file_name):
    # Convert the model to BDD
    fm = FeatureIDEParser(file_name).transform() 
    pysat_model = FmToPysat(fm).transform()
    cnf_model = PysatToCNF(pysat_model).transform()
    bdd_model = CNFToBDD(cnf_model).transform()

    print(cnf_model.get_cnf_formula())
    print("--------------------------")
    print(pysat_model.get_all_clauses())
    print(pysat_model.features)
    cnf_formula = []
    for c in pysat_model.get_all_clauses():
        cnf_formula.append(list(map(lambda l: 'Not ' + pysat_model.features[abs(l)] if l < 0 else pysat_model.features[abs(l)], c)))
    print(cnf_formula)

    # PYSAT number of solutions
    nof_solutions = len(Glucose3Products().execute(pysat_model).get_result())
    print(f'#Solutions: {nof_solutions}')

    # BDD number of solutions
    nof_solutions = BDDNumberOfConfigurations(fm).execute(bdd_model).get_result()
    print(f'#Solutions: {nof_solutions}')

    # BDD product distribution
    dist = BDDProductDistributionBF(fm).execute(bdd_model).get_result()
    print(f'Product Distribution: {dist}')

    # Create data
    x = range(len(fm.get_features())+1)
    y = dist

    # Plot
    plt.title("Product distribution")
    plt.xlabel("#Features")
    plt.ylabel("#Products")
    plt.plot(x, y, color='black')  # line plot
    plt.fill_between(x, y, color='grey')  # area plot
    plt.legend(loc="best")
    #plt.show()
    image_filename = 'pd_temp.png'
    plt.savefig(image_filename)

    # from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    # from matplotlib.figure import Figure

    # fig = Figure()
    # canvas = FigureCanvas(fig)
    # ax = fig.gca()

    # ax.text(0.0,0.0,"Test", fontsize=45)
    # ax.axis('off')

    # canvas.draw()       # draw the canvas, cache the renderer

    # image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')
    return image_filename


if __name__ == "__main__":
    logging.basicConfig(filename='famapybot.log', filemode='a+', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',)
    logging.info("FaMaPyBot is running...")

    bot = telebot.TeleBot(HTTP_API_TOKEN, parse_mode='MARKDOWN')

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
	    bot.reply_to(message, "Send me a feature model to analyze (in FeatureIDE .xml format).")

    @bot.message_handler(content_types=['document'])
    def analyze_feature_model(message):
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        content = requests.get(f'https://api.telegram.org/file/bot{HTTP_API_TOKEN}/{file_info.file_path}')

        if content.ok:
            with open(file_name, 'w+') as file:
                file.write(content.text)

            response = analyze_model(file_name)
            pd_image_filename = get_product_distribution(file_name)
            
            #bot.reply_to(message, response)
            photo = open(pd_image_filename, 'rb')
            bot.send_photo(chat_id=message.chat.id, photo=photo, caption=response, reply_to_message_id=message.id)

            if os.path.exists(file_name):
                os.remove(file_name)      
            if os.path.exists(pd_image_filename):
                os.remove(pd_image_filename)      

            #bot.reply_to(message, "Error processing the file.")
        else:
            bot.reply_to(message, "Error getting the file.")

    bot.polling()

    logging.info("FaMaPyBot has finished!")


