&Pgcod = 1
&Trmod = 666

Do 'Get transaction number'

&Trnom = 'GenAI defined'

&AccountinEntryJson.FromJson(&AccountinEntryJSONString)
//&Trnro = &AccountinEntryJson.Get(!"nro")
//&Trnom = &AccountinEntryJson.Get(!"nombre")
&ordinalsJson.FromJson(&AccountinEntryJson.Get(!"ordinals"))

Do 'Clear existent entry'

New //--FST034
Pgcod  = &Pgcod
Trmod  = &Trmod
Trnro  = &Trnro
Trnom  = &Trnom
Trhabt = 'N'
Trtext = 'N'
Trmn   = 'N'
Trme   = 'N'
Trreco = 'N'
Tropau = 'N'
Tromlm = 'N'
Trimpr = 'N'
Trcej  = 'N'
Trincr = 'S'
Trbjpa = 'S'
Trbjan = 'S'
Trccla = 'N'
Trnetp = 'N'
Triva  = 'N'
Trdtpo = 'N'
Trconf = 'S'
EndNew


For &ordinal in &ordinalsJson
    &Trord   = &ordinal.Get(!"nro").ToNumeric()
    &debeHab = &ordinal.Get(!"debe_hab")
	&Trdh = IIF(&debeHab = "db", 1, 2)

    &sucursalJson.FromJson(&ordinal.Get(!"sucursal"))
    &sucursalTipo = &sucursalJson.Get(!"tipo")

	&Trpsuc = 'M'
	&Trasuc = 0
	&Trfsuc = 0
    Do Case
        Case &sucursalTipo = "obtener de ordinal anterior"
			&Trpsuc = 'A'
			&Trasuc = &sucursalJson.Get(!"ordinal_nro").ToNumeric()
        Case &sucursalTipo = "obtener del preformato"
			&Trpsuc = 'P'
			&Trasuc = &sucursalJson.Get(!"preformato_nro").ToNumeric()
        Case &sucursalTipo = "obtener del preformato y pedir"
			&Trpsuc = 'Q'
			&Trasuc = &sucursalJson.Get(!"preformato_nro").ToNumeric()
        Case &sucursalTipo = "forzar valor"
			&Trpsuc = 'F'
			&Trfsuc = &sucursalJson.Get(!"valor").ToNumeric()
        Case &sucursalTipo = "obtener de la cuenta"
            &Trpsuc = 'C'
        Case &sucursalTipo = "solicitar"
            &Trpsuc = 'S'
    EndCase

    &especieJson.FromJson(&ordinal.Get(!"especie"))
    &especieTipo = &especieJson.Get(!"tipo")
	&Trppap = 'N'
	&Trapap = 0
	&Trfpap = 0
    Do Case
        Case &especieTipo = "solicitar"
            &Trppap = 'S'
        Case &especieTipo = "forzar valor"
            &Trppap = 'F'
            &Trfpap = &especieJson.Get(!"valor").ToNumeric()
        Case &especieTipo = "obtener de ordinal anterior"
            &Trppap = 'A'
            &Trapap = &especieJson.Get(!"ordinal_nro").ToNumeric()
        Case &especieTipo = "obtener del preformato"
            &Trppap = 'P'
            &Trapap = &especieJson.Get(!"preformato_nro").ToNumeric()
        Case &especieTipo = "obtener del preformato y pedir"
            &Trppap = 'Q'
            &Trapap = &especieJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &monedaJson.FromJson(&ordinal.Get(!"moneda"))
    &monedaTipo = &monedaJson.Get(!"tipo")
	&Trpmda = 'N'
	&Tramda = 0
	&Trfmda = 0
    Do Case
        Case &monedaTipo = "solicitar"
            &Trpmda = 'S'
        Case &monedaTipo = "forzar valor"
            &Trpmda = 'F'
            &Trfmda = &monedaJson.Get(!"valor").ToNumeric()
        Case &monedaTipo = "obtener de ordinal anterior"
            &Trpmda = 'A'
            &Tramda = &monedaJson.Get(!"ordinal_nro").ToNumeric()
        Case &monedaTipo = "obtener del preformato"
            &Trpmda = 'P'
            &Tramda = &monedaJson.Get(!"preformato_nro").ToNumeric()
        Case &monedaTipo = "obtener del preformato y pedir"
            &Trpmda = 'Q'
            &Tramda = &monedaJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &cuentaJson.FromJson(&ordinal.Get(!"cuenta"))
    &cuentaTipo = &cuentaJson.Get(!"tipo")
	&Trpcta = 'N'
	&Tracta = 0
	&Trfcta = 0
    Do Case
        Case &cuentaTipo = "solicitar"
            &Trpcta = 'S'
        Case &cuentaTipo = "forzar valor"
            &Trpcta = 'F'
            &Trfcta = &cuentaJson.Get(!"valor").ToNumeric()
        Case &cuentaTipo = "obtener de ordinal anterior"
            &Trpcta = 'A'
            &Tracta = &cuentaJson.Get(!"ordinal_nro").ToNumeric()
        Case &cuentaTipo = "obtener del preformato"
            &Trpcta = 'P'
            &Tracta = &cuentaJson.Get(!"preformato_nro").ToNumeric()
        Case &cuentaTipo = "obtener del preformato y pedir"
            &Trpcta = 'Q'
            &Tracta = &cuentaJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &nroOperacionJson.FromJson(&ordinal.Get(!"nroOperacion"))
    &nroOperacionTipo = &nroOperacionJson.Get(!"tipo")
	&Trpop = 'N'
	&Traop = 0
	&Trfop = 0
    Do Case
        Case &nroOperacionTipo = "solicitar"
            &Trpop = 'S'
        Case &nroOperacionTipo = "forzar valor"
            &Trpop = 'F'
            &Trfop = &nroOperacionJson.Get(!"valor").ToNumeric()
        Case &nroOperacionTipo = "obtener de ordinal anterior"
            &Trpop = 'A'
            &Traop = &nroOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &nroOperacionTipo = "obtener del preformato"
            &Trpop = 'P'
            &Traop = &nroOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &nroOperacionTipo = "obtener del preformato y pedir"
            &Trpop = 'Q'
            &Traop = &nroOperacionJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &subOperacionJson.FromJson(&ordinal.Get(!"subOperacion"))
    &subOperacionTipo = &subOperacionJson.Get(!"tipo")
	&Trpsop = 'N'
	&Trasop = 0
	&Trfsop = 0
    Do Case
        Case &subOperacionTipo = "solicitar"
            &Trpsop = 'S'
        Case &subOperacionTipo = "forzar valor"
            &Trpsop = 'F'
            &Trfsop = &subOperacionJson.Get(!"valor").ToNumeric()
        Case &subOperacionTipo = "obtener de ordinal anterior"
            &Trpsop = 'A'
            &Trasop = &subOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &subOperacionTipo = "obtener del preformato"
            &Trpsop = 'P'
            &Trasop = &subOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &subOperacionTipo = "obtener del preformato y pedir"
            &Trpsop = 'Q'
            &Trasop = &subOperacionJson.Get(!"preformato_nro").ToNumeric()
    EndCase

    &tipoOperacionJson.FromJson(&ordinal.Get(!"tipoOperacion"))
    &tipoOperacionTipo = &tipoOperacionJson.Get(!"tipo")
	&Trptop = 'N'
	&Tratop = 0
	&Trftop = 0
    Do Case
        Case &tipoOperacionTipo = "solicitar"
            &Trptop = 'S'
        Case &tipoOperacionTipo = "forzar valor"
            &Trptop = 'F'
            &Trftop = &tipoOperacionJson.Get(!"valor").ToNumeric()
        Case &tipoOperacionTipo = "obtener de ordinal anterior"
            &Trptop = 'A'
            &Tratop = &tipoOperacionJson.Get(!"ordinal_nro").ToNumeric()
        Case &tipoOperacionTipo = "obtener del preformato"
            &Trptop = 'P'
            &Tratop = &tipoOperacionJson.Get(!"preformato_nro").ToNumeric()
        Case &tipoOperacionTipo = "obtener del preformato y pedir"
            &Trptop = 'Q'
            &Tratop = &tipoOperacionJson.Get(!"preformato_nro").ToNumeric()
    EndCase

	New //--FST035 - TODO: Incluir campos con valores por defecto
	Pgcod    = &Pgcod
	Trmod    = &Trmod
	Trnro    = &Trnro
	Trord    = &Trord
	Trdh     = &Trdh
	Trordhab = 'S'
	Trpsuc   = &Trpsuc
	Trasuc   = &Trasuc
	Trfsuc   = &Trfsuc
	Trppap   = &Trppap
	Trapap   = &Trapap
	Trfpap   = &Trfpap
	Trpmda   = &Trpmda
	Tramda   = &Tramda
	Trfmda   = &Trfmda
	Trpcta   = &Trpcta
	Tracta   = &Tracta
	Trfcta   = &Trfcta
	Trpop    = &Trpop
	Traop    = &Traop
	Trfop    = &Trfop
	Trpsop   = &Trpsop
	Trasop   = &Trasop
	Trfsop   = &Trfsop
	Trptop   = &Trptop
	Tratop   = &Tratop
	Trftop   = &Trftop
	EndNew

    Do 'Add subordinal'
Endfor

Sub 'Add subordinal'
    &rubroJson.FromJson(&ordinal.Get(!"rubro"))
    &rubroTipo = &rubroJson.Get(!"tipo")
	&Trrubr    = 0
	&Trrcod    = 0
	&Trrord    = 0

    If &rubroTipo = "valor"
        &Trrubr = &rubroJson.Get(!"rubro").ToNumeric()
    Else // "relacionado"
        &Trrord = &rubroJson.Get(!"fromOrdinal").ToNumeric()
        &Trrcod = &rubroJson.Get(!"relCode").ToNumeric()
    EndIf

	&Trsbor = 10

	New //--FST036
	Pgcod  = &Pgcod
	Trmod  = &Trmod
	Trnro  = &Trnro
	Trord  = &Trord
	Trsbor = &Trsbor
	Trrubr = &Trrubr
	Trrcod = &Trrcod
	Trrord = &Trrord
	EndNew

EndSub

Sub 'Clear existent entry'
    For Each //--FST034
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Where Trnro = &Trnro
	Defined by Trnom
		Delete
    EndFor

    For Each //--FST035
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Where Trnro = &Trnro
	Defined by Trdh
		Delete
    EndFor

    For Each //--FST036
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Where Trnro = &Trnro
	Defined by Trrubr
		Delete
    EndFor
EndSub

Sub 'Get transaction number'
    &Trnro = 0
    For Each Order Pgcod, Trmod, Trnro //--FST034
    Where Pgcod = &Pgcod
	Where Trmod = &Trmod
	Defined by Trnom
		&Trnro = Trnro
    EndFor

    &Trnro = &Trnro + 1
EndSub
