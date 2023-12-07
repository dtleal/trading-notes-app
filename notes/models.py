from django.db import models
from djmoney.models.fields import MoneyField


class Asset(models.Model):
    """
    Model representing a financial asset.

    Attributes:
        symbol (CharField): Ticker symbol of the asset (e.g., AAPL for Apple Inc.).
        name (CharField): Name of the asset.
    """

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class Trigger(models.Model):
    """
    Model representing a trading trigger.
    """

    TRIGGER_CHOICES = [
        ("gap_ignored_bar", "Gap Ignored Bar"),
        ("powerful_candle", "Powerful Candle"),
        ("hammer_plus_averages", "Hammer + Averages"),
        ("open_gap_pb", "Open Gap Pullback"),
        ("open_gap_pb_averages", "Open Gap Pullback Averages"),
        ("perfect_pb", "Perfect Pullback"),
        ("scalp_pb", "Scalp Pullback"),
        ("stock_open_gap", "Stock Opening Gap"),
        ("stock_open_gap_breakout", "Stock Opening Gap Breakout Top/Bottom"),
    ]
    trigger = models.CharField(max_length=40, choices=TRIGGER_CHOICES)

    def __str__(self):
        return self.trigger


class Trade(models.Model):
    """
    Model representing a trading operation.

    Attributes:
        date_time (DateTimeField): Date and time of the operation.
        asset (CharField): Financial asset involved in the operation.
        side (CharField): Type of operation (buy or sell).
        trigger (CharField): Trigger for the operation (e.g., news, technical analysis).
        points_result (DecimalField): Result of the operation in points.
        dollars_result (DecimalField): Result of the operation in dollars.
        error (BooleanField): Indicates whether there was an error in the operation.
        description (TextField): Description or notes about the operation.
        image (ImageField): Optional image related to the operation.
    """

    date_time = models.DateTimeField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    side = models.CharField(
        max_length=10, choices=[("buy", "Compra"), ("sell", "Venda")]
    )
    lot_size = models.FloatField(default=0.0)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)
    points_result = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Enter the result as a percentage"
    )
    dollars_result = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    error = models.BooleanField()
    description = models.TextField()
    image = models.ImageField(upload_to="trade_images/", null=True, blank=True)
    # TODO: add bucket save
    #image = models.ImageField(upload_to="caminho/dentro/do/seu/bucket/", null=True, blank=True)

    def __str__(self):
        return f"{self.asset} - {self.date_time}"
