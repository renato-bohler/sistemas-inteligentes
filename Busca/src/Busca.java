// 1. Adicionar esta linha ao script do ambiente: simRemoteApi.start(19999)
// 2. Começar a simulação no V-REP
// 3. Executar este programa

import coppelia.IntW;
import coppelia.IntWA;
import coppelia.remoteApi;

public class Busca {
	public static void main(String[] args) {
		System.out.println("Program started");
		remoteApi vrep = new remoteApi();
		vrep.simxFinish(-1); // just in case, close all opened connections
		int clientID = vrep.simxStart("127.0.0.1", 19999, true, true, 5000, 5);
		if (clientID != -1) {
			System.out.println("Connected to remote API server");

			// Now try to retrieve data in a blocking fashion (i.e. a service
			// call):
			IntWA objectHandles = new IntWA(1);
			int ret = vrep.simxGetObjects(clientID, remoteApi.sim_handle_all,
					objectHandles, remoteApi.simx_opmode_blocking);
			if (ret == remoteApi.simx_return_ok)
				System.out.format("Number of objects in the scene: %d\n",
						objectHandles.getArray().length);
			else
				System.out
						.format("Remote API function call returned with error code: %d\n",
								ret);

			try {
				Thread.sleep(2000);
			} catch (InterruptedException ex) {
				Thread.currentThread().interrupt();
			}

			// Now retrieve streaming data (i.e. in a non-blocking fashion):
			long startTime = System.currentTimeMillis();
			IntW mouseX = new IntW(0);
			vrep.simxGetIntegerParameter(clientID,
					remoteApi.sim_intparam_mouse_x, mouseX,
					remoteApi.simx_opmode_streaming); // Initialize streaming
			while (System.currentTimeMillis() - startTime < 5000) {
				ret = vrep.simxGetIntegerParameter(clientID,
						remoteApi.sim_intparam_mouse_x, mouseX,
						remoteApi.simx_opmode_buffer); // Try to retrieve the
														// streamed data
				if (ret == remoteApi.simx_return_ok) // After initialization of
					// streaming, it will take a few
					// ms before the first value
					// arrives, so check the return
					// code
					System.out.format("Mouse position x: %d\n",
							mouseX.getValue()); // Mouse position x is
												// actualized when the cursor is
												// over V-REP's window
			}

			// Now send some data to V-REP in a non-blocking fashion:
			vrep.simxAddStatusbarMessage(clientID, "Hello V-REP!",
					remoteApi.simx_opmode_oneshot);

			// Before closing the connection to V-REP, make sure that the last
			// command sent out had time to arrive. You can guarantee this with
			// (for example):
			IntW pingTime = new IntW(0);
			vrep.simxGetPingTime(clientID, pingTime);

			// Now close the connection to V-REP:
			vrep.simxFinish(clientID);
		} else {
			System.out.println("Failed connecting to remote API server");
		}

		System.out.println("Program ended");
	}
}
