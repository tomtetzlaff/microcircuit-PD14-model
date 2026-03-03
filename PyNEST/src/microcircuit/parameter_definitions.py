## TODOs
##  - add "section" to json_schema_extra
##  -separate model and simulation parameters
##  -function for saving parameters to yaml
#    with open("outfile.yaml", "w") as outfile:
#       yaml.dump(params.model_dump(), outfile)
#    ## see also parameters of model_dump()

####################################

from ruamel.yaml import YAML
import numpy

from pydantic import BaseModel, Field, computed_field
import rich

####################################


class Parameters(BaseModel):

    #########################################################################
    ## network parameters

    N_scaling: float = Field(
        default=1.0,
        description="Scaling factor determining network size.",
        json_schema_extra={"unit": "", "latex": r"$\alpha_N$", "section": r"network"},
    )

    K_scaling: float = Field(
        default=1.0,
        description="Scaling factor determining synapse numbers.",
        json_schema_extra={"unit": "", "latex": r"$\alpha_K$", "section": r"network"},
    )

    populations: list = Field(
        default=["L23E", "L23I", "L4E", "L4I", "L5E", "L5I", "L6E", "L6I"],
        description="List of population names.",
        json_schema_extra={
            "unit": "",
            "latex": r"$\mathcal{P}=\Bigcup_x x$",
            "section": r"network",
        },
    )

    full_num_neurons: list = Field(
        default=[20683, 5834, 21915, 5479, 4850, 1065, 14395, 2948],
        description="Default number of neurons in each population.",
        json_schema_extra={
            "unit": "",
            "latex": r"$\tilde{N}_x$ ($\forall x\in\mathcal{P}$)",
            "section": r"network",
        },
    )

    conn_probs: list = Field(
        default=[
            [0.1009, 0.1689, 0.0437, 0.0818, 0.0323, 0.0, 0.0076, 0.0],
            [0.1346, 0.1371, 0.0316, 0.0515, 0.0755, 0.0, 0.0042, 0.0],
            [0.0077, 0.0059, 0.0497, 0.135, 0.0067, 0.0003, 0.0453, 0.0],
            [0.0691, 0.0029, 0.0794, 0.1597, 0.0033, 0.0, 0.1057, 0.0],
            [0.1004, 0.0622, 0.0505, 0.0057, 0.0831, 0.3726, 0.0204, 0.0],
            [0.0548, 0.0269, 0.0257, 0.0022, 0.06, 0.3158, 0.0086, 0.0],
            [0.0156, 0.0066, 0.0211, 0.0166, 0.0572, 0.0197, 0.0396, 0.2252],
            [0.0364, 0.001, 0.0034, 0.0005, 0.0277, 0.008, 0.0658, 0.1443],
        ],
        description="Connection probabilities (first index: target; second index: source)",
        json_schema_extra={
            "unit": "",
            "latex": r"$C_{yx}$ ($\forall y,x\in\mathcal{P}$)",
            "section": r"network",
        },
    )

    #########################################################################
    ## neuron parameters
    neuron_model: str = Field(
        default="iaf_psc_exp",
        description="NEST neuron model name.",
        json_schema_extra={
            "unit": "",
            "latex": r"neuron\_model",
            "section": r"neuron",
        },
    )

    ## TODO: adjust model code to the new parameterization used here
    ## (in the old version, all neuron parameters were kept in a dictionary neuron_params, including the initial conditions)

    ## TODO: rename variable into `V_rest`
    E_L: float = Field(
        default=-65.0,
        description="Resting potential.",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$E_\text{L}$",  ## TODO: use V_\text{rest}
            "section": r"neuron",
        },
    )

    V_th: float = Field(
        default=-50.0,
        description="Spike threshold potential.",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$\theta$",  ## TODO: use V_\text{th}
            "section": r"neuron",
        },
    )

    V_reset: float = Field(
        default=-65.0,
        description="After-spike reset potential.",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$V_\text{reset}$",
            "section": r"neuron",
        },
    )

    C_m: float = Field(
        default=250.0,
        description="Membrane capacitance.",
        json_schema_extra={
            "unit": "pF",
            "latex": r"$C_\text{m}$",
            "section": r"neuron",
        },
    )

    tau_m: float = Field(
        default=10.0,
        description="Membrane time constant.",
        json_schema_extra={
            "unit": "ms",
            "latex": r"$\tau_\text{m}$",
            "section": r"neuron",
        },
    )

    ## TODO: rename variable into `tau_ref`
    t_ref: float = Field(
        default=2.0,
        description="Duration of absolute refractory period.",
        json_schema_extra={
            "unit": "ms",
            "latex": r"$\tau_\text{ref}$",
            "section": r"neuron",
        },
    )

    #########################################################################
    ## synapse parameters

    ## TODO: rename variable into `weight_exc_mean`
    PSP_exc_mean: float = Field(
        default=0.15,
        description="Mean weight of excitatory synapses (PSP amplitude).",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$J$",
            "section": r"synapse",
        },
    )

    ## TODO: rename variable into `weight_cv`
    weight_rel_std: float = Field(
        default=0.1,
        description="Coefficient of variation of synaptic weight distributions (ratio between standard deviation and mean).",
        json_schema_extra={
            "unit": "",
            "latex": r"$\text{CV}_\text{w}$",
            "section": r"synapse",
        },
    )

    g: float = Field(
        default=-4.0,
        description="Relative weight of inhibitory synapses (ratio of inhibitory and excitatory synaptic weights).",
        json_schema_extra={
            "unit": "",
            "latex": r"$g$",
            "section": r"synapse",
        },
    )

    tau_syn: float = Field(
        default=0.5,
        description="Time constant of postsynaptic currents.",
        json_schema_extra={
            "unit": "ms",
            "latex": r"$\tau_\text{s}$",
            "section": r"synapse",
        },
    )

    delay_exc_mean: float = Field(
        default=1.5,
        description="Mean spike transmission delay of excitatory connections.",
        json_schema_extra={
            "unit": "ms",
            "latex": r"$\bar{d}_\text{E}$",
            "section": r"synapse",
        },
    )

    delay_inh_mean: float = Field(
        default=0.75,
        description="Mean spike transmission delay of inhibitory connections.",
        json_schema_extra={
            "unit": "ms",
            "latex": r"$\bar{d}_\text{I}$",
            "section": r"synapse",
        },
    )

    ## TODO: rename variable into `delay_cv`
    delay_rel_std: float = Field(
        default=0.5,
        description="Coefficient of variation of delay distributions (ratio between standard deviation and mean).",
        json_schema_extra={
            "unit": "",
            "latex": r"$\text{CV}_\text{d}$",
            "section": r"synapse",
        },
    )

    #########################################################################
    ## initialization parameters

    V0_type: str = Field(
        default="optimized",
        description=r"Type of initial condition for the membrane potentials ('original' or 'optimized'). 'original': uniform mean and standard deviation for all populations. 'optimized': population-specific mean and standard deviation (default).",
        json_schema_extra={
            "unit": "",
            "latex": r"V0\_type",
            "section": r"initialization",
        },
    )

    ## TODO: adjust model code to the new parameterization used here
    V0_mean_original: float = Field(
        default=-58.0,
        description="Mean of initial membrane potentials in case V0_type = 'original'.",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$V0\_mean\_original$",
            "section": r"initialization",
        },
    )

    V0_std_original: float = Field(
        default=10.0,
        description="Standard deviation of initial membrane potentials in case V0_type = 'original'.",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$V0\_std\_original$",
            "section": r"initialization",
        },
    )

    V0_mean_optimized: list = Field(
        default=[-68.28, -63.16, -63.33, -63.45, -63.11, -61.66, -66.72, -61.43],
        description="Population-specific mean of initial membrane potentials in case V0_type = 'optimized' (same order as in `populations`).",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$V0\_mean\_optimized$",
            "section": r"initialization",
        },
    )

    V0_std_optimized: list = Field(
        default=[5.36, 4.57, 4.74, 4.94, 4.94, 4.55, 5.46, 4.48],
        description="Population-specific standard deviation of initial membrane potentials in case V0_type = 'optimized' (same order as in `populations`).",
        json_schema_extra={
            "unit": "mV",
            "latex": r"$V0\_std\_optimized$",
            "section": r"initialization",
        },
    )

    #########################################################################
    ## stimulus parameters
    full_mean_rates: list = Field(
        default=[0.903, 2.965, 4.414, 5.876, 7.569, 8.633, 1.105, 7.829],
        description="Mean firing rates of the different populations in the non-scaled version of the microcircuit (same order as in `populations`; required for network scaling).",
        json_schema_extra={
            "unit": "spikes/s",
            "latex": r"$\nu_x$ ($\forall x\in\mathcal{P}$)",
            "section": r"stimulus",
        },
    )

    ## TODO: rename variable into `cc_type`
    bg_input_type: str = Field(
        default="dc",
        description="Type of cortico-cortical input ('poisson' or 'dc').",
        json_schema_extra={
            "unit": "",
            "latex": r"bg\_input\_type",
            "section": r"stimulus",
        },
    )

    ## TODO: rename variable into `K_cc`
    K_ext: list = Field(
        default=[1600, 1500, 2100, 1900, 2000, 1900, 2900, 2100],
        description="Number of cortico-cortical inputs per neuron (in-degree) for the different populations (same order as in `populations`).",
        json_schema_extra={
            "unit": "",
            "latex": r"$K_{\mathcal{C}_x}$ ($\forall x\in\mathcal{P}$)",
            "section": r"stimulus",
        },
    )

    ## TODO: rename variable into `rate_cc`
    bg_rate: float = Field(
        default=8.0,
        description="Rate of cortico-cortical inputs.",
        json_schema_extra={
            "unit": "spikes/s",
            "latex": r"$\nu_\mathcal{C}$",
            "section": r"stimulus",
        },
    )

    ## TODO: rename variable into `delay_cc`
    delay_poisson: float = Field(
        default=1.5,
        description="Spike transmission delay of cortico-cortical inputs.",
        json_schema_extra={
            "unit": "ms",
            "latex": r"$\bar{d}_{yx}$ ($\forall y\in\mathcal{P},\ x=\mathcal{C}_y$)",
            "section": r"stimulus",
        },
    )

    ## TODO: remaining stimululs parameters

    #########################################################################
    ## simulation parameters
    ## TODO

    #########################################################################
    ### computed fields for derived parameters
    @computed_field(
        description="Number of neurons in each population.",
        json_schema_extra={
            "unit": "",
            "latex": r"$N_i=\alpha_N \tilde{N}_i$ ($\forall i\in\mathcal{P}$)",
            "section": r"network",
        },
    )
    @property
    def num_neurons(self) -> list:
        return (self.N_scaling * numpy.array(self.full_num_neurons)).astype(int)

    ## TODO: R_m
    ## TODO: PSP_matrix_mean
    ## TODO: delay_matrix_mean
    ## TODO: t_stop
    ## TODO: synaptic weights $\bar{I})yx$ (PSC amplitude) for different pairs $x$ and $y$
    ## TODO: mean total current of cc inputs $I_{C_x}$
    ## TODO: mean current of each individual cc input

    # def model_post_init(self):
    #     assert self.J>0


####################################
def generate_example_config(filename="params_default.yaml", mode="validation") -> None:
    schema = Parameters.model_json_schema(mode=mode)

    with open(filename, "w") as yaml_file:
        yaml_file.write("# This file is autogenerated by generate_example_config().\n")
        yaml_file.write(
            "# To modify the metadata (descriptions, units, LaTeX symbols),\n"
        )
        yaml_file.write(
            "# edit the parameters definition in parameter_definitions.py,\n"
        )
        yaml_file.write("# and run generate_example_config() again.\n")
        yaml_file.write("\n")

        for key in schema["properties"].keys():
            field = schema["properties"][key]

            if "default" in field:
                yaml_file.write(f"{key}: {field['default']}\n")
            else:
                yaml_file.write(f"# {key}: This is a derived parameter.\n")

            yaml_file.write(f"# {field['description']}\n")
            yaml_file.write(f"# unit: {field['unit']}\n")
            yaml_file.write(f"# LaTeX: {field['latex']}\n")
            yaml_file.write(f"# section: {field['section']}\n")
            yaml_file.write("\n")


####################################
## move to io.py
yaml = YAML()


def load_parameters_from_yaml(filename) -> Parameters:
    with open(filename, "r") as yaml_file:
        loaded_params = yaml.load(yaml_file)
        return Parameters.model_validate(loaded_params)


def test_parameter_loading(filename):

    params = Parameters()

    # filename = "params_default.yaml"
    # generate_example_config(filename)

    test_params = load_parameters_from_yaml(filename)

    assert (
        params == test_params
    ), "Validation failed: Loaded parameters do not match the original defaults."


####################################

if __name__ == "__main__":
    filename = "params_default.yaml"
    generate_example_config(filename, mode="validation")

    test_parameter_loading(filename)
    print("All tests passed.")
    P = load_parameters_from_yaml(filename)

    rich.print(P)
