from pydantic import BaseModel


class Note(BaseModel):
    frequency: float
    duration: float
    note: int  # 0-127


if __name__ == '__main__':
    nota = Note(frequency=544, duration=2, note=2)
    print(nota)
