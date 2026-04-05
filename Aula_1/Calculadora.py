from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        a = dados.get("num1")
        b = dados.get("num2")
        operacao = dados.get("operacao")

        if a is None or b is None or operacao is None:
            return jsonify({"erro": "Parâmetros obrigatórios: num1, num2 e operacao"}), 400

        a = float(a)
        b = float(b)

        if operacao == "soma":
            resultado = a + b

        elif operacao == "subtracao":
            resultado = a - b

        elif operacao == "multiplicacao":
            resultado = a * b

        elif operacao == "divisao":
            if b == 0:
                return jsonify({"erro": "Divisão por zero"}), 400
            resultado = a / b

        else:
            return jsonify({"erro": "Operação inválida"}), 400

        return jsonify({
            "num1": a,
            "num2": b,
            "operacao": operacao,
            "resultado": resultado
        })

    except ValueError:
        return jsonify({"erro": "Os valores devem ser números"}), 400

    except Exception as e:
        return jsonify({
            "erro": "Erro interno no servidor",
            "detalhes": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
