import logging

def configure_logging(name):
    #Establecemos el formato que tendrán los mensajes de log
    logFormatter = logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s [\t%(name)s.%(funcName)s:%(lineno)d]\t %(message)s')

    #Creamos el logger
    logger = logging.getLogger(name)
    #Indicamos el level de errores que queremos que muestre el log
    logger.setLevel(logging.INFO)

    #Manejador para grabar los mensajes en ficheros
    fileHandler = logging.FileHandler("logs.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    #Manejador para mostrar los mensajes por consola
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    #Devolvemos el logger
    return logger