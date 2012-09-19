class ConfigOptions(object):
    """
    An enumeration of sorts to hold the section and option names for the config file.
    """
    test_section = 'TEST'
    output_folder_option = 'output_folder'
    data_file_option = "data_file"
    repetitions_option = "repeat"
    recovery_time_option = "recovery_time"
    
    dut_section = 'NODE1'
    test_interface_option = "test_interface"
    operating_system_option = "operating_system"
    control_ip_option = "hostname"
    test_ip_option = "test_ip"
    connection_option = 'connection'
    traffic_pc_section = "TRAFFIC_PC"
    login_option = "login"
    password_option = "password"

    logwatcher_section = "LOGWATCHER"
    paths_option = "paths"

    logcatwatcher_section = "LOGCATWATCHER"
    buffers_option = "buffers"

    nodes_section = "NODES"
    
    iperf_section = "IPERF"
    directions_option = "directions"
    window_option = "window"
    length_option = "length"
    parallel_option = "parallel"
    interval_option = "interval"
    format_option = "format"
    time_option = "time"

    affector_section = "AFFECTOR"
    affector_type_option = "type"
    switches_option = "switches"
    hostname_option = "hostname"
