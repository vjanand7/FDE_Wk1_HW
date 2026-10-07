import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Invoice API")

DATA_FILE = "data/invoices.json"



class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    status: str = "PENDING"


def load_invoices():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_invoices(invoices):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(invoices, f, indent=2)


@app.get("/invoices")
def get_invoices():
    return load_invoices()


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    for invoice in load_invoices():
        if invoice["invoice_id"] == invoice_id:
            return invoice
    raise HTTPException(status_code=404, detail="Invoice not found")


@app.post("/invoices", status_code=201)
def create_invoice(invoice: Invoice):
    invoices = load_invoices()
    if any(i["invoice_id"] == invoice.invoice_id for i in invoices):
        raise HTTPException(status_code=409, detail="Invoice already exists")
    new_invoice = invoice.model_dump()
    invoices.append(new_invoice)
    save_invoices(invoices)
    return {"message": "Invoice created successfully", "invoice": new_invoice}


@app.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: str):
    invoices = load_invoices()
    remaining = [i for i in invoices if i["invoice_id"] != invoice_id]
    if len(remaining) == len(invoices):
        raise HTTPException(status_code=404, detail="Invoice not found")
    save_invoices(remaining)
    return {"message": f"Invoice {invoice_id} deleted"}
