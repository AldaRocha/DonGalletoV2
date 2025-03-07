using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace Servicios.Entidad.Model
{
    public class Receta
    {
        [Key]
        public int RecetaId { get; set; }
		public decimal Cantidad { get; set; }
        public int GalletaId { get; set; }
        public virtual Galleta Galleta { get; set; }
	    public int InventarioId { get; set; }
        public virtual Inventario Inventario { get; set; }
        public int MedidaId { get; set; }
        public virtual Medida Medida { get; set; }
    }
}
