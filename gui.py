import numpy as np
import tkinter as tk
from tkinter import messagebox,ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from analysis.psd import align_spectra,apply_bandwidth,compute_psd
from analysis.ssc import compute_ssc
from signals.boc import generate_boc
from signals.bpsk import generate_bpsk_signal
from signals.mboc import generate_mboc


class GnssApp:
    def __init__(self,root):
        self.root=root
        self.root.title("GNSS Spectrum Visualizer")

        self.root.geometry("1380x880")
        self.root.minsize(1200,780)
        self.root.configure(background="#f4f5f7")



        self.demo_center_frequency=tk.StringVar(value="1575.42e6")

        self.demo_transmitter_bandwidth=tk.StringVar(value="24e6")
        self.demo_receiver_bandwidth=tk.StringVar(value="24e6")
        self.demo_sampling_frequency=tk.StringVar(value="100e6")

        self.demo_num_bits=tk.StringVar(value="2048")
        self.demo_comparison_signal=tk.StringVar(value="MBOC(6,1,1/11)")



        self.center_frequency=tk.StringVar(value="1575.42e6")
        self.transmitter_bandwidth=tk.StringVar(value="24e6")
        self.receiver_bandwidth=tk.StringVar(value="24e6")
        self.sampling_frequency=tk.StringVar(value="100e6")

        self.num_bits=tk.StringVar(value="2048")



        self.boc_m=tk.StringVar(value="5")
        self.boc_n=tk.StringVar(value="2")
        self.comparison_type=tk.StringVar(value="MBOC")

        self.bpsk_multiple=tk.StringVar(value="10")
        self.mboc_component1_m=tk.StringVar(value="1")

        self.mboc_component1_n=tk.StringVar(value="1")
        self.mboc_component1_weight=tk.StringVar(value="10/11")
        self.mboc_component2_m=tk.StringVar(value="6")
        self.mboc_component2_n=tk.StringVar(value="1")

        self.mboc_component2_weight=tk.StringVar(value="1/11")



        self.result_text=tk.StringVar(value="SSC: -")
        self.view_center_frequency=tk.DoubleVar(value=1575.42e6)

        self.view_slider_text=tk.StringVar(value="Slider")
        self.view_window_span_hz=20e6

        self.current_freq_min=None
        self.current_freq_max=None
        self.overlay_freqs_boc=None
        
        self.overlay_psd_boc=None
        self.overlay_freqs_comp=None
        self.overlay_psd_comp=None

        self.overlay_label=""


        self.build_layout()
        self.build_figure()
        self.run_demo_analysis()




    def build_layout(self):
        st=ttk.Style()
        st.theme_use("clam")
        st.configure("Header.TLabel",font=("Helvetica",16,"bold"),background="#f4f5f7")
        st.configure("Card.TLabelframe",background="#ffffff")

        st.configure("Card.TLabelframe.Label",font=("Helvetica",11,"bold"))

        root=tk.Frame(self.root,padx=16,pady=16,background="#f4f5f7")
        root.pack(fill="both",expand=True)

        head=ttk.Label(root,text="GNSS Spectrum Visualizer and Interference Analysis",style="Header.TLabel")
        head.pack(anchor="w",pady=(0,10))

        body=ttk.Frame(root)
        body.pack(fill="both",expand=True)

        left=ttk.Frame(body,width=380)
        left.grid(row=0,column=0,sticky="ns",padx=(0,14))

        self.plot_box=ttk.Frame(body)
        self.plot_box.grid(row=0,column=1,sticky="nsew")
        body.columnconfigure(1,weight=1)

        body.rowconfigure(0,weight=1)

        self.tabs=ttk.Notebook(left)
        self.tabs.pack(fill="both",expand=False)

        self.demo_tab=ttk.Frame(self.tabs,padding=10)
        self.an_tab=ttk.Frame(self.tabs,padding=10)

        self.tabs.add(self.demo_tab,text="Demo Cases")
        self.tabs.add(self.an_tab,text="Custom Analysis")


        self.build_demo_tab(self.demo_tab)
        self.build_analysis_tab(self.an_tab)

        box=ttk.LabelFrame(left,text="SSC",style="Card.TLabelframe",padding=12)
        box.pack(fill="x",pady=(14,0))

        ttk.Label(box,textvariable=self.result_text,justify="left",wraplength=330).pack(anchor="w")




    def build_figure(self):
        self.plot_box.rowconfigure(0,weight=0)

        self.plot_box.rowconfigure(1,weight=1)
        self.plot_box.columnconfigure(0,weight=1)

        sbox=ttk.Frame(self.plot_box,padding=(8,8,8,6))
        sbox.grid(row=0,column=0,sticky="ew")

        ttk.Label(sbox,textvariable=self.view_slider_text).pack(anchor="w")
        self.view_slider=tk.Scale(sbox,orient="horizontal",showvalue=False,resolution=100000.0,command=self.on_slider,length=760)
        self.view_slider.pack(fill="x",expand=True)

        pbox=ttk.LabelFrame(self.plot_box,text="Normalized PSD and Overlap",style="Card.TLabelframe",padding=10)
        pbox.grid(row=1,column=0,sticky="nsew")
        pbox.rowconfigure(0,weight=1)

        pbox.columnconfigure(0,weight=1)

        self.figure=Figure(figsize=(10.5,8.0),dpi=100,facecolor="white",constrained_layout=True)
        self.overlay_axis=self.figure.add_subplot(211)
        self.overlap_axis=self.figure.add_subplot(212)

        self.canvas=FigureCanvasTkAgg(self.figure,master=pbox)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0,sticky="nsew")

    def add_entry(self,parent,lbl,var,row):
        ttk.Label(parent,text=lbl).grid(row=row,column=0,sticky="w",pady=(0,4))
        ent=ttk.Entry(parent,textvariable=var,width=24)
        ent.grid(row=row,column=1,sticky="we",pady=(0,4))



    def build_demo_tab(self,parent):
        intro=ttk.Label(parent,text="Demo Signals",wraplength=330,justify="left")
        intro.pack(anchor="w",pady=(0,10))

        frm=ttk.LabelFrame(parent,text="Demo Inputs",style="Card.TLabelframe",padding=12)
        frm.pack(fill="x")

        self.add_entry(frm,"Center freq (Hz)",self.demo_center_frequency,0)
        self.add_entry(frm,"Transmitter Bandwidth (Hz)",self.demo_transmitter_bandwidth,1)
        self.add_entry(frm,"Receiver Bandwidth (Hz)",self.demo_receiver_bandwidth,2)

        self.add_entry(frm,"Sampling freq (Hz)",self.demo_sampling_frequency,3)
        self.add_entry(frm,"Number of Bits",self.demo_num_bits,4)

        ttk.Label(frm,text="Comparison Signal").grid(row=5,column=0,sticky="w",pady=(10,4))
        cmb=ttk.Combobox(frm,textvariable=self.demo_comparison_signal,values=["MBOC(6,1,1/11)","BPSK(10)"],state="readonly",width=22)
        cmb.grid(row=6,column=0,columnspan=2,sticky="we")

        row=ttk.Frame(frm)
        row.grid(row=7,column=0,columnspan=2,sticky="we",pady=(14,0))
        row.columnconfigure(0,weight=1)
        ttk.Button(row,text="Run Demo",command=self.run_demo_analysis).grid(row=0,column=0,sticky="we")



    def build_analysis_tab(self,parent):
        intro=ttk.Label(parent,text="Custom analysis",wraplength=330,justify="left")
        intro.pack(anchor="w",pady=(0,10))

        frm=ttk.LabelFrame(parent,text="Signal Parameters",style="Card.TLabelframe",padding=12)
        frm.pack(fill="x")

        self.add_entry(frm,"Center freq",self.center_frequency,0)
        self.add_entry(frm,"Transmitter Bandwidth (Hz)",self.transmitter_bandwidth,1)
        self.add_entry(frm,"Receiver Bandwidth (Hz)",self.receiver_bandwidth,2)
        self.add_entry(frm,"Sampling freq",self.sampling_frequency,3)
        self.add_entry(frm,"Number of Bits",self.num_bits,4)

        bfrm=ttk.LabelFrame(parent,text="Reference BOC(m,n)",style="Card.TLabelframe",padding=12)
        bfrm.pack(fill="x",pady=(10,0))
        self.add_entry(bfrm,"m",self.boc_m,0)
        self.add_entry(bfrm,"n",self.boc_n,1)

        cfrm=ttk.LabelFrame(parent,text="Comparison Signal",style="Card.TLabelframe",padding=12)
        cfrm.pack(fill="x",pady=(10,0))

        ttk.Label(cfrm,text="Type").grid(row=0,column=0,sticky="w",pady=(0,4))
        cmb=ttk.Combobox(cfrm,textvariable=self.comparison_type,values=["MBOC","BPSK"],state="readonly",width=22)
        cmb.grid(row=0,column=1,sticky="we",pady=(0,4))

        self.bpsk_box=ttk.Frame(cfrm)
        self.mboc_box=ttk.Frame(cfrm)

        self.add_entry(self.bpsk_box,"BPSK Multiple",self.bpsk_multiple,0)
        self.add_entry(self.mboc_box,"MBOC Component 1 m",self.mboc_component1_m,0)
        self.add_entry(self.mboc_box,"MBOC Component 1 n",self.mboc_component1_n,1)

        self.add_entry(self.mboc_box,"MBOC Component 1 weight",self.mboc_component1_weight,2)
        self.add_entry(self.mboc_box,"MBOC Component 2 m",self.mboc_component2_m,3)
        self.add_entry(self.mboc_box,"MBOC Component 2 n",self.mboc_component2_n,4)

        self.add_entry(self.mboc_box,"MBOC Component 2 weight",self.mboc_component2_weight,5)

        self.bpsk_box.grid(row=1,column=0,columnspan=2,sticky="we")
        self.mboc_box.grid(row=1,column=0,columnspan=2,sticky="we")



        def flip(event=None):
            if self.comparison_type.get()=="BPSK":
                self.bpsk_box.grid()
                self.mboc_box.grid_remove()
            else:
                self.mboc_box.grid()
                self.bpsk_box.grid_remove()

        cmb.bind("<<ComboboxSelected>>",flip)

        row=ttk.Frame(parent)
        row.pack(fill="x",pady=(12,0))
        row.columnconfigure(0,weight=1)
        ttk.Button(row,text="Run Custom Analysis",command=self.run_analysis).grid(row=0,column=0,sticky="we")



    def load_demo_values(self):
        self.demo_center_frequency.set("1575.42e6")
        self.demo_transmitter_bandwidth.set("24e6")

        self.demo_receiver_bandwidth.set("24e6")
        self.demo_sampling_frequency.set("100e6")
        self.demo_num_bits.set("2048")

        self.demo_comparison_signal.set("MBOC(6,1,1/11)")

        self.center_frequency.set("1575.42e6")
        self.transmitter_bandwidth.set("24e6")
        self.receiver_bandwidth.set("24e6")
        self.sampling_frequency.set("100e6")
        self.num_bits.set("2048")

        self.boc_m.set("5")
        self.boc_n.set("2")

        self.comparison_type.set("MBOC")

        self.bpsk_multiple.set("10")


        self.mboc_component1_m.set("1")
        self.mboc_component1_n.set("1")
        self.mboc_component1_weight.set("1/11")
        self.mboc_component2_m.set("6")
        self.mboc_component2_n.set("1")
        self.mboc_component2_weight.set("10/11")
        self.tabs.select(self.demo_tab)
        self.run_demo_analysis()

    def parse_float(self,var,lbl):
        try:
            return float(var.get())
        except ValueError as e:
            raise ValueError(f"{lbl} must be a number") from e

    def parse_int(self,var,lbl):
        try:
            val=int(var.get())
        except ValueError as e:
            raise ValueError(f"{lbl} must be an integer") from e
        if val<=0:
            raise ValueError(f"{lbl} must be positive")
        return val

    def parse_weight(self,var,lbl):
        txt=var.get().strip()
        if "/" in txt:
            a,b=txt.split("/",1)
            try:
                n=float(a)
                d=float(b)
            except ValueError as e:
                raise ValueError(f"{lbl} must be a number or fraction") from e
            if d==0:
                raise ValueError(f"{lbl} denominator must not be zero")
            return n/d
        try:
            return float(txt)
        except ValueError as e:
            raise ValueError(f"{lbl} must be a number or fraction") from e

    def build_comp_sig(self,fs,n,prefix):
        if prefix=="demo":
            sel=self.demo_comparison_signal.get()
            if sel=="BPSK(10)":
                return generate_bpsk_signal(n,10*1.023e6,fs),"BPSK(10)"
            comps=[{"m":1,"n":1,"weight":1/11},{"m":6,"n":1,"weight":10/11}]
            return generate_mboc(comps,n,fs),"MBOC(6,1,1/11)"

        sel=self.comparison_type.get()
        if sel=="BPSK":
            mul=self.parse_int(self.bpsk_multiple,"BPSK Multiple")
            return generate_bpsk_signal(n,mul*1.023e6,fs),f"BPSK({mul})"

        comps=[
            {"m":self.parse_int(self.mboc_component1_m,"MBOC Component 1 m"),"n":self.parse_int(self.mboc_component1_n,"MBOC Component 1 n"),"weight":self.parse_weight(self.mboc_component1_weight,"MBOC Component 1 weight")},
            {"m":self.parse_int(self.mboc_component2_m,"MBOC Component 2 m"),"n":self.parse_int(self.mboc_component2_n,"MBOC Component 2 n"),"weight":self.parse_weight(self.mboc_component2_weight,"MBOC Component 2 weight")},
        ]
        return generate_mboc(comps,n,fs),"MBOC"

    def run_pipeline(self,cf,tbw,rbw,fs,n,prefix):
        if prefix=="demo":
            m=5
            k=2
        else:
            m=self.parse_int(self.boc_m,"BOC m")
            k=self.parse_int(self.boc_n,"BOC n")

        if m<=0 or k<=0:
            raise ValueError("BOC parameters must be positive")

        boc_sig=generate_boc(m,k,n,fs)
        comp_sig,comp_lbl=self.build_comp_sig(fs,n,prefix)

        boc_freqs,boc_psd=compute_psd(boc_sig,fs,center_frequency=cf)
        comp_freqs,comp_psd=compute_psd(comp_sig,fs,center_frequency=cf)

        boc_freqs,boc_psd=apply_bandwidth(boc_freqs,boc_psd,cf,tbw)
        comp_freqs,comp_psd=apply_bandwidth(comp_freqs,comp_psd,cf,tbw)

        boc_freqs,boc_psd,comp_freqs,comp_psd=align_spectra(boc_freqs,boc_psd,comp_freqs,comp_psd)
        cut=min(len(boc_freqs),len(comp_freqs))
        boc_freqs=boc_freqs[:cut]
        comp_freqs=comp_freqs[:cut]
        boc_psd=boc_psd[:cut]
        comp_psd=comp_psd[:cut]

        ssc=compute_ssc(boc_psd,comp_psd,boc_freqs,center_frequency=cf,receiver_bandwidth=rbw)

        ssc_db=10*np.log10(ssc) if ssc>0 else float("-inf")
        ssc_db_text=f"{ssc_db:.6f} dB" if np.isfinite(ssc_db) else "-inf dB"

        self.result_text.set(f"SSC: {ssc:.3e}\nSSC dB: {ssc_db_text}\nReference: BOC({m},{k}) vs {comp_lbl}")
        self.plot_results(boc_freqs,boc_psd,comp_freqs,comp_psd,ssc,ssc_db,comp_lbl,cf,rbw)




    def plot_results(self,boc_freqs,boc_psd,comp_freqs,comp_psd,ssc,ssc_db,comp_lbl,cf,rbw):
        self.overlap_axis.clear()

        self.overlay_freqs_boc=boc_freqs
        self.overlay_psd_boc=boc_psd
        self.overlay_freqs_comp=comp_freqs
        self.overlay_psd_comp=comp_psd
        self.overlay_label=comp_lbl

        ov=boc_psd*comp_psd
        lo=cf-rbw/2
        hi=cf+rbw/2
        self.overlap_axis.plot(boc_freqs,ov,color="#2ca02c",linewidth=1.2,label="PSD overlap")
        self.overlap_axis.axvspan(lo,hi,color="#d62728",alpha=0.12,label="Receiver band")
        ssc_db_text=f"{ssc_db:.2f} dB" if np.isfinite(ssc_db) else "-inf dB"
        self.overlap_axis.set_title(f"SSC overlap   |  SSC = {ssc:.3e}  |  {ssc_db_text}")
        self.overlap_axis.set_xlabel("Frequency (Hz)")
        self.overlap_axis.set_ylabel("PSD product")
        self.overlap_axis.grid(True,alpha=0.3)
        self.overlap_axis.legend(loc="upper right")

        self.current_freq_min=min(boc_freqs[0],comp_freqs[0]) if len(boc_freqs) and len(comp_freqs) else None
        self.current_freq_max=max(boc_freqs[-1],comp_freqs[-1]) if len(boc_freqs) and len(comp_freqs) else None

        if comp_lbl.startswith("BPSK"):
            self.view_window_span_hz=max(20e6,rbw)
        else:
            self.view_window_span_hz=max(14e6,rbw*0.75)

        self.configure_slider(cf)
        self.apply_view_window(self.view_center_frequency.get())
        self.canvas.draw_idle()




    def configure_slider(self,cf):
        if self.current_freq_min is None or self.current_freq_max is None:
            return

        half=self.view_window_span_hz/2
        lo=self.current_freq_min+half
        hi=self.current_freq_max-half

        if hi<=lo:
            back=max(self.view_window_span_hz,2e6)
            center=cf if cf!=0 else (self.current_freq_min+self.current_freq_max)/2
            self.view_slider.configure(from_=center-back/2,to=center+back/2)
            self.view_slider.set(center)
            self.view_center_frequency.set(center)
            self.view_slider_text.set(f"Slider  |  Value: {center/1e6:.3f} MHz")
            return

        self.view_slider.configure(from_=lo,to=hi)
        center=cf if cf!=0 else (lo+hi)/2
        self.view_slider.set(center)
        self.view_center_frequency.set(center)
        self.view_slider_text.set(f"Slider  |  Value: {center/1e6:.3f} MHz")



    def apply_view_window(self,cf):
        if self.current_freq_min is None or self.current_freq_max is None:
            return

        if cf == 0 and self.current_freq_min != 0 and self.current_freq_max != 0:
            cf = (self.current_freq_min + self.current_freq_max) / 2

        half=self.view_window_span_hz/2
        lo=max(self.current_freq_min,cf-half)
        hi=min(self.current_freq_max,cf+half)

        if hi<=lo:
            lo=self.current_freq_min
            hi=self.current_freq_max

        self.redraw_overlay_axis(lo,hi)
        self.overlap_axis.set_xlim(lo,hi)
        self.canvas.draw_idle()



    def redraw_overlay_axis(self,lo,hi):
        if self.overlay_freqs_boc is None or self.overlay_freqs_comp is None:
            return

        self.overlay_axis.clear()

        boc_mask=(self.overlay_freqs_boc>=lo)&(self.overlay_freqs_boc<=hi)
        comp_mask=(self.overlay_freqs_comp>=lo)&(self.overlay_freqs_comp<=hi)

        boc_freqs=self.overlay_freqs_boc[boc_mask]
        boc_psd=self.overlay_psd_boc[boc_mask]
        comp_freqs=self.overlay_freqs_comp[comp_mask]
        comp_psd=self.overlay_psd_comp[comp_mask]

        boc_display=self.scale_for_display(boc_psd)
        comp_display=self.scale_for_display(comp_psd)


        self.overlay_axis.plot(boc_freqs,boc_display,color="#1f77b4",linewidth=1.2,label="BOC(5,2)")
        self.overlay_axis.plot(comp_freqs,comp_display,color="#ff7f0e",linewidth=1.2,label=self.overlay_label)
        self.overlay_axis.set_title("Overlay of normalized PSDs")
        self.overlay_axis.set_ylabel("PSD (display-scaled)")
        self.overlay_axis.grid(True,alpha=0.3)
        self.overlay_axis.legend(loc="upper right")
        self.overlay_axis.set_xlim(lo,hi)



    def scale_for_display(self,vals):
        if len(vals)==0:
            return vals

        peak=float(vals.max())
        if peak<=0:
            return vals

        return vals/peak



    def on_slider(self,value):

        try:
            cf=float(value)
            self.view_center_frequency.set(cf)
        except ValueError:
            return

        self.view_slider_text.set(f"Slider  |  Value: {cf/1e6:.3f} MHz")
        self.apply_view_window(cf)




    def run_demo_analysis(self):
        try:
            cf=self.parse_float(self.demo_center_frequency,"Center Frequency")
            tbw=self.parse_float(self.demo_transmitter_bandwidth,"Transmitter Bandwidth")
            rbw=self.parse_float(self.demo_receiver_bandwidth,"Receiver Bandwidth")
            fs=self.parse_float(self.demo_sampling_frequency,"Sampling Frequency")

            n=self.parse_int(self.demo_num_bits,"Number of Bits")

            if fs<=0:
                raise ValueError("Sampling Frequency must be positive")
            
            if tbw<=0:
                raise ValueError("Transmitter Bandwidth must be positive")
            if rbw<=0:
                raise ValueError("Receiver Bandwidth must be positive")

            self.run_pipeline(cf,tbw,rbw,fs,n,"demo")
            self.tabs.select(self.demo_tab)
        except ValueError as err:
            messagebox.showerror("Input error",str(err))

    def run_analysis(self):
        try:
            cf=self.parse_float(self.center_frequency,"Center Frequency")
            tbw=self.parse_float(self.transmitter_bandwidth,"Transmitter Bandwidth")

            rbw=self.parse_float(self.receiver_bandwidth,"Receiver Bandwidth")
            fs=self.parse_float(self.sampling_frequency,"Sampling Frequency")
            n=self.parse_int(self.num_bits,"Number of Bits")

            if fs<=0:
                raise ValueError("Sampling Frequency must be positive")
            if tbw<=0:
                raise ValueError("Transmitter Bandwidth must be positive")
            

            if rbw<=0:
                raise ValueError("Receiver Bandwidth must be positive")

            self.run_pipeline(cf,tbw,rbw,fs,n,"analysis")
            self.tabs.select(self.an_tab)
        except ValueError as err:
            messagebox.showerror("Input error",str(err))




def launch_gui():
    root=tk.Tk()
    GnssApp(root)
    root.mainloop()