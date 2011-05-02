typedef struct{
	float4 point; // x, y, z,  radius
	float4 color; // r, g, b, a
} SphereData;

float4 matmul(global const float4 *m, const float4 r1) {
	return (float4)(dot(m[0],r1),dot(m[1],r1),dot(m[2],r1),dot(m[3],r1));
}

__constant float EPSILON = 1e-5;
__constant float PI = 3.1415;
g
// Main Kernel code
kernel void pdbTracer(
	global uchar4 *img,
	global const float4 *m,	// inverted camera matrix
	global const float4 *minv,
	int nSpheres,
	global const SphereData *spheres,
	read_only image2d_t envmap,
	read_only image2d_t phimap,
	sampler_t sampler
)
{	
	unsigned int x = get_global_id(0);
  unsigned int y = get_global_id(1);
	unsigned int width = get_global_size(0);
	unsigned int height = get_global_size(1);
	unsigned int index = (y * width) + x;

	float u = ((x+0.5) / (float) width)*2.0f-1.0f; // 0.5 increment is to reach the center of the pixel.
	float v = ((y+0.5) / (float) height)*2.0f-1.0f;
	
	// Ray vector assuming 90 degree viewing angle (image plane at z=-1)
	float4 d = matmul(minv, (float4)(u,v,-1,0));
	d = normalize(d);
	
	// The camera center
	float4 p = matmul(minv, (float4)(0,0,0,1));
	
	float4 color = 0;
	float mint = MAXFLOAT;
	int mini = 0;
	for (int i = 0; i < nSpheres; i++) {
		// Geometric method, due to http://www.devmaster.net/wiki/Ray-sphere_intersection
		float r = spheres[i].point.w;
		float4 c = spheres[i].point; c.w = 1; // garbage in the w position here, from packing
		float4 oc = c - p; oc.w = 0;
		float loc2 = dot(oc,oc);
		if (loc2 < r*r) continue; // Starting inside the sphere!
		float tca = dot(d, oc);
		if (tca < 0) continue; // Sphere center is behind us
		float lhc2 = r*r - loc2 + tca*tca;
		if (lhc2 < 0) continue; // Missed!
		float t = tca - sqrt(lhc2);
		if (t < mint) {
			mint = t;
			mini = i;
		}
	}
	// Find the normal, if we have a hit
	if (mint < MAXFLOAT) {
		float4 N = p + mint * d - spheres[mini].point; N.w = 0;
		//N = normalize(N);
		//float f = -dot(N,d); // Pretend the sun is always behind us
		//color = spheres[mini].color * f;
		//img[index] = convert_uchar4_sat_rte(color*255.0f);
		
		//float4 dir = normalize(matmul(m, d - 2 * dot(N,d) * N)); 
		N = normalize(matmul(m, N));
		
		// These don't have correct dimensions but it doesn't matter
		float4 bx = normalize(cross(N, (float4)(1,0,0,0)));
		float4 by = normalize(cross(bx,N));
		
		float4 sum = (float4) 0;
		float NX1 = 20;
		float NX2 = 20;
		for (float x1 = 0; x1 < 1; x1 += 1.0f/NX1) {
			for (float x2 = 0; x2 < 1; x2 += 1.0f/NX2) {
				float2 tcp = (float2)(x1, x2);
				float4 c = read_imagef(phimap, sampler, tcp);
				float4 dir = normalize(c.x*bx + c.y*by + c.z*N);
				
				float r = (1/PI)*acos(dir.z)/sqrt(dir.x*dir.x+dir.y*dir.y+EPSILON);
				float2 tc = (float2)(0.5*dir.x*r + 0.5, 0.5*dir.y*r + 0.5);
				sum += read_imagef(envmap, sampler, tc);
			}
		}
		color = sum / (NX1 * NX2 * 2);
	} else {
		float4 dir = normalize(matmul(m, d));
		//float4 dir = d;
		float r = (1/PI)*acos(dir.z)/sqrt(dir.x*dir.x + dir.y*dir.y+EPSILON);
		float2 tc = (float2)(0.5*dir.x*r + 0.5, 0.5*dir.y*r + 0.5);
		color = read_imagef(envmap, sampler, tc);
	}
	img[index] = convert_uchar4_sat_rte(color*255.0f);
}
