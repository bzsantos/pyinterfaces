# pyinterfaces

A lightweight Python compiler extension that brings clean, Java-style interface syntax to Python using native braces `{}`.

[![PyPI version](https://shields.io)](https://pypi.org)
[![Python Versions](https://shields.io)](https://pypi.org)

---

## 📐 Why pyinterfaces? (Software Engineering Perspective)

In modern **Software Engineering**, separating *definition* from *implementation* is a core architectural principle. 
Following SOLID principles—specifically the **Interface Segregation Principle (ISP)** and the **Dependency Inversion Principle (DIP)**—software components should depend on abstractions (interfaces), not on concrete logic.

While standard Python uses `abc.ABC` and `@abstractmethod` to enforce contracts, the syntax can often look cluttered, repetitive, and conceptually muddy (as Python abstract classes can accidentally mix actual logic with abstract models).

**`pyinterfaces`** bridges this gap by enforcing **Pure Interfaces**. It allows software engineers to declare strict structural contracts using the familiar, elegant, and universally understood Java/C# layout, keeping your architecture clean and highly readable.

---

## ✨ Features

- **Java-Style Syntax**: Declare structures using `Interface Name { ... }`.
- **Pure Abstraction**: No mixed implementation code allowed inside the contract block.
- **Runtime Enforcement**: Automatically triggers native Python `abc` validations under the hood.
- **Zero Overhead**: Translated seamlessly during file tokenization using custom stream decoding.

---

## 🚀 Installation

You can install `pyinterfaces` via `pip` or add it to your project using `poetry`:

```bash
pip install pyinterfaces
```

- Poetry:
```bash
poetry add pyinterfaces or python -m poetry add pyinterfaces
```
##Directories

Project start:

```bash
- PIP:
pyinterfaces-init

- Poetry:
poetry pyinterfaces-init
```

```bash
- PIP:
pyinterfaces-generate app
- Poetry:
poetry pyinterfaces-generate app
```

- my_project/
- ├── modules/
- │   └── app/
- │       ├── __init__.py
- │       ├── interfaces.py     # Interfaces / Contract (ML Inputs & Outputs)
- │       ├── repository.py     # 🧠 @Repository (Loads scikit-learn/onnx and runs predict)
- │       ├── service.py        # @Service (Applies business rules before/after ML)
- │       ├── controller.py     # @RestController (Receives the JSON to be predicted)
- │       └── views/
- │           └── index.html    # UI interface (Dashboard to show ML insights)
- └── main.py                   # IoC Container bootstrap
  
---

## 💻 Usage

To enable the custom Java-like syntax parsing, you **must** include the magic encoding comment `# -*- coding: java_interface -*-` at the very first line of your Python script.

Here is a standard example of designing a decoupled Payment System:

```python
# -*- coding: java_interface -*-
import pyinterfaces

# 1. Define the pure architectural contract
Interface PaymentProcessor {
    process_payment(self, amount: float) -> bool
    refund_payment(self, transaction_id: str) -> None
}

# 2. Implement the contract in standard Python classes
class PixProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing R\${amount} instantly via Pix.")
        return True

    def refund_payment(self, transaction_id: str) -> None:
        print(f"Refunding transaction {transaction_id}.")

# 3. Compile-time / Runtime validation
class BrokenProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        return True
    # ERROR! Missing 'refund_payment' method implementation.
```

If a developer attempts to instantiate `BrokenProcessor`, Python will instantly raise a `TypeError`, stating that the class failed to implement the strict contract requirements defined by your interface.

---

## 🛠️ How it works under the hood

`pyinterfaces` hooks directly into Python's native `codecs` registry. When the interpretator reads the `# -*- coding: java_interface -*-` header, it streams your file through our custom pre-processor, safely transforming the custom block syntax into fully valid standard Python `abc.ABC` structures before the code even executes.

---

## 👤 Author

- Created and maintained by **Bruno Zolotareff**
- PyPI Repository: [https://pypi.org](https://pypi.org)

## 🤝 Acknowledgments

Special thanks to my friend **Leandro Reginaldo** for collaborating on the original concept, brainstorming the architectural ideas, and helping to shape the vision of `pyinterfaces`. This project wouldn't be the same without your insights!


## 📄 License

This project is licensed under the MIT License.
