from utca.implementation.tasks import TransformersTextClassification

if __name__ == "__main__":
    res = TransformersTextClassification().run({
        "inputs": "Stocks rallied and the British pound gained.",
    })

    print(res)