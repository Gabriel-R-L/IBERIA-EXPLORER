from django.db import models

class Carrito(models.Model):
    from appLoginRegistro.models import Usuario
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Carrito"
        verbose_name_plural = "Carrito"
        
    def __str__(self):
        return f"{self.id_carrito}, {self.id_usuario}"
    
        
        
class CarritoDetalle(models.Model):
    from appIberiaExplorer.models import Plan
    id_carrito_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "CarritoDetalle"
        verbose_name_plural = "CarritoDetalles"
        
    def __str__(self):
        return f"{self.id_carrito_detalle}, {self.cantidad}, {self.id_carrito}, {self.id_plan}"
    


class Pedido(models.Model):
    from appLoginRegistro.models import Usuario
    ESTADOS_PEDIDO = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ]
        
    id_pedido = models.AutoField(primary_key=True)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    estado = models.CharField(max_length=10, choices=ESTADOS_PEDIDO, default='PENDIENTE')
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        
    def __str__(self):
        return f"{self.id_pedido}, {self.fecha_reserva}, {self.total}, {self.id_cliente}, {self.estado}"
        
        
class PedidoDetalle(models.Model):
    from appIberiaExplorer.models import Plan
    id_pedido_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        managed = True
        verbose_name = "PedidoDetalle"
        verbose_name_plural = "PedidoDetalles"
        
    def __str__(self):
        return f"{self.id_pedido_detalle}, {self.id_pedido}, {self.id_plan}, {self.cantidad}"
