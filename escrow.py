class EscrowManager:
    def __init__(self, commission_percent):
        self.escrows = {}  # escrow_id: {seller_id, buyer_id, amount, status}
        self.user_balances = {}  # user_id: trx_balance
        self.next_id = 1
        self.commission_percent = commission_percent

    def create_escrow(self, seller_id, amount):
        escrow_id = self.next_id
        self.escrows[escrow_id] = {
            "seller_id": seller_id,
            "buyer_id": None,
            "amount": amount,
            "status": "waiting_buyer"
        }
        self.next_id += 1
        return escrow_id

    def assign_buyer(self, escrow_id, buyer_id):
        if escrow_id not in self.escrows:
            raise Exception("Escrow bulunamadı.")
        escrow = self.escrows[escrow_id]
        if escrow["status"] != "waiting_buyer":
            raise Exception("Escrow alıcı beklemiyor.")
        escrow["buyer_id"] = buyer_id
        escrow["status"] = "pending"

    def approve(self, escrow_id, user_id):
        escrow = self.escrows.get(escrow_id)
        if not escrow:
            raise Exception("Escrow bulunamadı.")
        if user_id != escrow["buyer_id"]:
            raise Exception("Bu işlemi onaylamaya yetkiniz yok.")
        escrow["status"] = "completed"
        amount = escrow["amount"]
        commission = int(amount * self.commission_percent / 100)
        net_amount = amount - commission
        seller_id = escrow["seller_id"]
        self.user_balances[seller_id] = self.user_balances.get(seller_id, 0) + net_amount
        return net_amount, commission

    def dispute(self, escrow_id, user_id):
        escrow = self.escrows.get(escrow_id)
        if not escrow:
            raise Exception("Escrow bulunamadı.")
        if user_id != escrow["buyer_id"]:
            raise Exception("Bu işlemi onaylamaya yetkiniz yok.")
        escrow["status"] = "dispute"
        # Admin müdahalesi demo olarak burada yapılacak

    def get_balance(self, user_id):
        return self.user_balances.get(user_id, 0)
